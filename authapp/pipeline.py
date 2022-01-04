from collections import OrderedDict
from datetime import datetime
from urllib.parse import urlencode, urlunparse

import requests
from django.conf import settings
from django.utils import timezone
from social_core.exceptions import AuthForbidden

from authapp.models import UserProfile


# bdate
# about
# sex
def save_user_profile(backend, user, response, *args, **kwargs):
    if backend.name != 'vk-oauth2':  # проверка соцсети
        return

    api_url = urlunparse(('http', 'api.vk.com', 'method/users.get', None,
                          urlencode(OrderedDict(fields=','.join(('bdate', 'sex', 'about', 'personal', 'photo_max_orig')),
                                                access_token=response['access_token'], v=5.131)), None))

    # api_url = f'https://api.vk.com/method/users.get/?fields=bdate,sex,about&access_token={response["access_token"]}&v=5.131'

    response = requests.get(api_url)
    if response.status_code != 200:
        return

    data = response.json()['response'][0]
# получение пола пользователя
    if data['sex'] == 1:
        user.userprofile.gender = UserProfile.FEMALE
    elif data['sex'] == 2:
        user.userprofile.gender = UserProfile.MALE
    else:
        pass

    # получение фото
    if 'photo_max_orig' in data:
        photo_content = requests.get(data['photo_max_orig'])  # получение адреса фото на странице
        with open(f'{settings.MEDIA_ROOT}/users_image/{user.pk}.jpg', 'wb') as photo_file:
            photo_file.write(photo_content.content)
            user.image = f'users_image/{user.pk}.jpg'

# получение about
    if data['about']:
        user.userprofile.about = data['about']

# получение возраста
    bdate = datetime.strptime(data['bdate'], '%d.%m.%Y').date()
    age = timezone.now().date().year - bdate.year

    user.age = age

    if age < 18:
        user.delete()
        raise AuthForbidden('social_core.backends.vk.VKOAuth2')

    # получение языка пользователя
    if data['personal']['langs']:
        user.userprofile.langs = data['personal']['langs'][0] if len(data['personal']['langs'][0]) > 0 else 'EN'

    user.save()


