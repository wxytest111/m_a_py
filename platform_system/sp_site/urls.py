# -*- coding: utf-8 -*-

from django.conf.urls import patterns, include, url
from sp_site.views import *
from platform_system import settings

urlpatterns = patterns('',
    #商品管理
    url(r'^product_manage$', product_manage,name="product_manage"), 
    url(r'^product_list$', product_list,name="product_list"), 
    url(r'^order_list$', order_list,name="order_list"), 
    url(r'^change_login_pwd$', change_login_pwd,name="change_login_pwd"),
    
    url(r'^logout$', logout,name="logout"),
    url(r'^login$', login,name="login"), 
    url(r'^$', index,name="index"),
)

if settings.DEBUG:
    import debug_toolbar
    urlpatterns += patterns('',
        url(r'^__debug__/', include(debug_toolbar.urls)),
    )