# -*- coding: utf-8 -*-
# @Author: DELL
# @Date:   2019-01-04 16:23:21
# @Last Modified by:   DELL
# @Last Modified time: 2019-01-15 21:27:23
from django.urls import re_path
from . import views

urlpatterns = [
    re_path(r'^register/$', views.register),
    re_path(r'^register_handle/$', views.register_handle),
    re_path(r'^check_uname/$', views.check_uname),
    re_path(r'^login/$', views.login),
    re_path(r'^login_check/$', views.login_check),
    re_path(r'^login_handle/$', views.login_handle),
    re_path(r'^user_center_info/$', views.user_center_info),
    re_path(r'^user_center_order_(\d+)/$', views.user_center_order),
    re_path(r'^user_center_site/$', views.user_center_site),
    re_path(r'^logout/$', views.logout),
]
