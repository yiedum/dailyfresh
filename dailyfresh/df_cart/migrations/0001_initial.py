# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('df_goods', '0001_initial'),
        ('df_user', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='CartInfo',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, serialize=False, verbose_name='ID')),
                ('count', models.IntegerField()),
                ('goods', models.ForeignKey(to='df_goods.GoodsInfo', on_delete=models.CASCADE)),
                ('user', models.ForeignKey(to='df_user.userinfo', on_delete=models.CASCADE)),
            ],
        ),
    ]
