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
            name='OrderDetail',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('oprice', models.DecimalField(decimal_places=2, max_digits=5)),
                ('ocount', models.IntegerField()),
                ('goods', models.ForeignKey(to='df_goods.GoodsInfo', on_delete=models.CASCADE)),
            ],
        ),
        migrations.CreateModel(
            name='OrderInfo',
            fields=[
                ('oid', models.CharField(max_length=20, primary_key=True, serialize=False)),
                ('odate', models.DateTimeField(auto_now=True)),
                ('ocost', models.DecimalField(decimal_places=2, max_digits=6)),
                ('ispay', models.BooleanField(default=False)),
                ('user', models.ForeignKey(to='df_user.userinfo', on_delete=models.CASCADE)),
            ],
        ),
        migrations.AddField(
            model_name='orderdetail',
            name='order',
            field=models.ForeignKey(to='df_order.OrderInfo', on_delete=models.CASCADE),
        ),
    ]
