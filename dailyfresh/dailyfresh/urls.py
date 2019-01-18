from django.urls import include, re_path
from django.contrib import admin

urlpatterns = [
    re_path(r'^admin/', admin.site.urls),
    re_path(r'^user/', include('df_user.urls')),
    re_path(r'^', include('df_goods.urls')),
    re_path(r'^', include('df_cart.urls')),
    re_path(r'^', include('df_order.urls')),
    re_path(r'^search/', include('haystack.urls')),
]
