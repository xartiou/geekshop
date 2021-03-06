# Generated by Django 3.2.8 on 2022-01-04 10:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authapp', '0003_auto_20211229_2034'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='langs',
            field=models.CharField(blank=True, max_length=10, null=True, verbose_name='язык'),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='gender',
            field=models.CharField(blank=True, choices=[('M', 'МУЖ'), ('W', 'ЖЕН')], max_length=3, verbose_name='пол'),
        ),
    ]
