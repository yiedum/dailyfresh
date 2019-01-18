# -*- coding: utf-8 -*-
# @Author: DELL
# @Date:   2019-01-04 16:23:21
# @Last Modified by:   DELL
# @Last Modified time: 2019-01-15 21:27:01
from django.urls import re_path
from . import views

urlpatterns = [
    re_path(r'^order/$', views.order),
    re_path(r'^order_submit/$', views.order_submit),
]
