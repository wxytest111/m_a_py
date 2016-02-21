#coding:utf8
from django.shortcuts import render_to_response
from django.template import  RequestContext
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.contrib import auth
from django.core.urlresolvers import reverse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from forms import *
from models.models import *
from views import check_login

import json
import hashlib
from datetime import datetime
import time

import logging
logger = logging.getLogger('admin_site')



@check_login
def subc_list(request):
    '''
    查询预订列表
    '''
    
    
    

    template_args = {}

    return render_to_response('admin_site/subscribe_list.html', 
        {'template_args': template_args}, context_instance=RequestContext(request)
        )
        
        

@check_login
def edit_subc(request):
    '''
    编辑预订信息
    '''
    
    ret = {}
    return HttpResponse(json.dumps(ret), content_type='application/json')

        

        
@check_login
def order_list(request):
    '''
    查询订单记录
    '''
    
    
    template_args = {}

    return render_to_response('admin_site/order_list.html', 
        {'template_args': template_args}, context_instance=RequestContext(request)
        )
        


@check_login
def edit_order(request):
    '''
    修改订单信息
    '''
    
    ret = {}
    return HttpResponse(json.dumps(ret), content_type='application/json')

        
        
        
@check_login
def product_list(request):
    '''
    商品列表查询
    '''
    
    template_args = {}

    return render_to_response('admin_site/product_list.html', 
        {'template_args': template_args}, context_instance=RequestContext(request)
        )

        
        
@check_login
def add_prod(request):
    '''
    添加商品
    '''
    
    ret = {}
    return HttpResponse(json.dumps(ret), content_type='application/json')

    


@check_login
def edit_prod(request):
    '''
    编辑商品信息
    '''
    
    
    ret = {}
    return HttpResponse(json.dumps(ret), content_type='application/json')

    

@check_login
def edit_prod_state(request):
    '''
    修改商品状态
    '''
    
    
    ret = {}
    return HttpResponse(json.dumps(ret), content_type='application/json')
