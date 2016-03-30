#coding:utf8
from django.shortcuts import render_to_response
from django.template import  RequestContext
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect,HttpResponse
from django.contrib import auth
from django.core.urlresolvers import reverse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q
from django.core.urlresolvers import reverse
from django.core.files.base import ContentFile

from forms import *
from models.models import *
from views import check_login
import json
import logging
logger = logging.getLogger('admin_site')

@check_login
def product_list(request):
    '''
    商品列表查询
    '''
    
    template_args = {}

    if "application/json" in request.META["HTTP_ACCEPT"]:
        start = int(request.GET["start"])
        length = int(request.GET["length"])
        key = request.GET.get("search[value]")
        order_desc = request.GET.get("columns[4][orderable]")

        product_list = Products.objects.filter()
        if key :
            product_list = product_list.filter(name__contains=key)

        total_count = product_list.count()

        if order_desc == 'true' and request.GET.get("order[0][column]") == "4":
            if  request.GET.get("order[0][dir]") == "asc":
                product_list = product_list.order_by("created_at")
            else:
                product_list = product_list.order_by("-created_at")

        if order_desc == 'true' and request.GET.get("order[0][column]") == "3":
            if request.GET.get("order[0][dir]") == "asc":
                product_list = product_list.order_by("state")
            else:
                product_list = product_list.order_by("-state")

        product_list = product_list[start:start+length]
                
        template_args["draw"] = int(request.GET.get("draw","0"))
        template_args["recordsTotal"] = int(total_count)
        template_args["recordsFiltered"] = int(total_count)
        template_args["data"] = []

        for item in product_list:
            x = {}
            x["id"] = item.id
            x["name"] = item.name
            x["show_price"] = item.show_price
            x["pay_price"] = item.pay_price
            x["display_state"] = item.get_state_display()
            x["created_at"] = None if not item.created_at else item.created_at.strftime("%Y-%m-%d %H:%M:%S")

            template_args["data"].append(x)

        return HttpResponse(json.dumps(template_args), content_type='application/json')
    else:
        return render_to_response('admin_site/product_list.html', 
            {'template_args': template_args}, context_instance=RequestContext(request)
            )

        
        
@check_login
def add_prod(request):
    '''
    添加商品
    '''
    template_args={}
    if request.method  == "POST":
        form = ProductForm(request.POST,request.FILES)
        if form.is_valid():
            cd = form.cleaned_data
            form.save()

            return HttpResponseRedirect(reverse("admin_site:product_list"))

        template_args["form"] = form
    else:
        template_args["form"] = ProductForm()

    return render_to_response('admin_site/prod_add.html',
        {'template_args': template_args}, context_instance=RequestContext(request)
        )

@check_login
def edit_prod(request):
    '''
    编辑商品信息
    '''

    template_args={}
    if request.method  == "POST":
        form = ProductForm(request.POST,request.FILES,instance=Products.objects.get(pk=request.GET.get("id")))
        if form.is_valid():
            cd = form.cleaned_data
            form.save()

            return HttpResponseRedirect(reverse("admin_site:product_list"))

        template_args["form"] = form
    else:
        template_args["form"] = ProductForm(instance=Products.objects.get(pk=request.GET.get("id")))

    return render_to_response('admin_site/prod_add.html',
        {'template_args': template_args}, context_instance=RequestContext(request)
        )

@check_login
def edit_prod_state(request):
    '''
    修改商品状态
    '''
    
    
    ret = {}

    prod = Products.objects.get(pk=request.GET.get("id"))
    if request.GET.get("type") == "1":
        prod.state = 2;
    else:
        if prod.state != 1:
            prod.state = 3;

    prod.save()

    ret["retcode"] = "0"
    ret["retmsg"] = "success"
    return HttpResponse(json.dumps(ret), content_type='application/json')
