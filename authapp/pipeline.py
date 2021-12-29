from collections import OrderedDict
from datetime import datetime
from urllib.parse import urlencode, urlunparse

import requests
from django.utils import timezone
from social_core.exceptions import AuthForbidden

from authapp.models import UserProfile


# bdate
# about
# sex
def save_user_profile(backend, user, response, *args, **kwargs):
    if backend.name != 'vk-oauth2':  # проверка соцсети
        return

    # api_url = urlunparse(('http', 'api.vk.com', 'method/users.get', None,
    #                       urlencode(OrderedDict(fields=','.join(('bdate', 'sex', 'about')),
    #                                             access_token=response['access_token'], v=5.131)), None))

    api_url = f'https://api.vk.com/method/users.get/?fields=bdate,sex,about&access_token={response["access_token"]}&v=5.131'

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
    user.save()
