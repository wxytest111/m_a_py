# -*- coding: utf-8 -*-

from django.conf.urls import patterns, include, url
from admin_site.views import *
from admin_site.order_manage_views import *
from admin_site.shop_manage_views import *
from admin_site.user_manage_views import *
from platform_system import settings

urlpatterns = patterns('',
    #管理员列表
    url(r'^admin_list$', admin_list,name="admin_list"),

    #审核
    url(r'^shop_verify_list$', shop_verify_list, name="shop_verify_list"),
    url(r'^shop_verify_history$', shop_verify_history, name="shop_verify_history"),
    url(r'^shop_verify$', audit_shop_apply, name="audit_shop_apply"),

    
    #店铺
    url(r'^shop_list$', shop_list,name="shop_list"),
    url(r'^shop_detail$', shop_detail, name="shop_detail"),
    url(r'^edit_shop$', edit_shop, name="edit_shop"),


    #订单
    ###查询所有订单
    url(r'^order_list$', order_list,name="order_list"),
    ###修改订单详情
    url(r'^edit_order$', edit_order,name="edit_order"),
    
    
    #预订
    ###查询所有预订
    url(r'^subc_list$', subc_list,name="subc_list"),
    ###编辑预订记录
    url(r'^edit_subc$', edit_subc,name="edit_subc"),


    #买家管理
    url(r'^customer_list$', customer_list,name="customer_list"),
    
    
    #商品管理
    url(r'^product_list$', product_list,name="product_list"),
    url(r'^add_prod$', add_prod,name="add_prod"),
    url(r'^edit_prod$', edit_prod,name="add_prod"),
    url(r'^edit_prod_state$', edit_prod_state,name="edit_prod_state"),
    

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