# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2018-01-18 04:44
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0005_auto_20171230_1412'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='friends',
            field=models.ManyToManyField(related_name='_userprofile_friends_+', to='web.UserProfile'),
        ),
    ]
