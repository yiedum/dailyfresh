# -*- coding: utf-8 -*-
# @Author: DELL
# @Date:   2019-01-04 16:23:21
# @Last Modified by:   DELL
# @Last Modified time: 2019-01-16 16:26:53
from django.urls import re_path
from . import views

urlpatterns = [
    re_path(r'^$', views.index),
    re_path(r'^list_(\d)_(\d+)_(\d)/$', views.list),
    re_path(r'^detail_(\d+)/$', views.detail),
    re_path(r'^cart_count/$', views.cart_count),
]
