# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='userinfo',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True, serialize=False)),
                ('uname', models.CharField(max_length=20)),
                ('upwd', models.CharField(max_length=40)),
                ('uemail', models.CharField(max_length=30)),
                ('ushou', models.CharField(default='', max_length=20)),
                ('uaddress', models.CharField(default='', max_length=100)),
                ('uphone', models.CharField(default='', max_length=11)),
                ('isDelete', models.BooleanField(default=False)),
            ],
        ),
    ]
