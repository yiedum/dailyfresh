# -*- coding: utf-8 -*-
# @Author: DELL
# @Date:   2019-01-04 16:23:21
# @Last Modified by:   DELL
# @Last Modified time: 2019-01-15 21:25:48
from django.urls import re_path
from . import views

urlpatterns = [
    re_path(r'^cart/$', views.cart),
    re_path(r'^add_(\d+)_(\d+)/$', views.add),
    re_path(r'^update_(\d+)_(\d+)/$', views.update),
    re_path(r'^delete_(\d+)/$', views.delete),
]
