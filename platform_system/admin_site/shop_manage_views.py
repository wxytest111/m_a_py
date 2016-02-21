#coding:utf8
from django.shortcuts import render_to_response
from django.template import  RequestContext
from django.contrib.auth.models import User
from django.http import HttpResponse,HttpResponseRedirect
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
from django.db.models import Q

import logging
logger = logging.getLogger('admin_site')

#@check_login
def shop_list(request):
    '''
    查询所有已审核商铺
    '''
    template_args = {}
    if "application/json" in request.META["HTTP_ACCEPT"]:
        start = int(request.GET["start"])
        length = int(request.GET["length"])
        key = request.GET.get("search[value]")
        order_desc = request.GET.get("columns[3][orderable]")

        shop_all = Shops.objects.filter()
        if key :
            shop_all = shop_all.filter(Q(name__contains=key)|Q(title__contains=key)|Q(tel__contains=key))

        total_count = shop_all.count()

        if order_desc == 'true' and request.GET.get("order[0][column]") == "3" and request.GET.get("order[0][dir]") == "asc":
            shop_all = shop_all.order_by("created_at")
        else:
            shop_all = shop_all.order_by("-created_at")

        shop_all = shop_all[start:start+length]
                
        template_args["draw"] = int(request.GET.get("draw","0"))
        template_args["recordsTotal"] = int(total_count)
        template_args["recordsFiltered"] = int(total_count)
        template_args["data"] = []

        for shop in shop_all:
            x = {}
            x["id"] = shop.id
            x["name"] = shop.name
            x["tel"] = shop.tel
            x["title"] = shop.title
            x["create_at"] = shop.created_at.strftime("%Y-%m-%d")
            x["uuid"] = shop.uuid
            template_args["data"].append(x)

        return HttpResponse(json.dumps(template_args), content_type='application/json')
    else:
        return render_to_response('admin_site/shop_list.html', 
            {'template_args': template_args}, context_instance=RequestContext(request)
            )

#@check_login
def shop_detail(request):
    '''
    查询店铺相信信息
    '''
    
    ret = {}
    
    shop_id = request.GET.get("id", None)
    if not shop_id:
        ret["retcode"] = "1000"
        ret["retmsg"] = "缺少输入参数"
        return HttpResponse(json.dumps(ret), content_type='application/json')
      
    try:
        shop_info = Shops.objects.get(id=shop_id)
    except ObjectDoesNotExist:
        ret["retcode"] = "1001"
        ret["retmsg"] = "未找到待审核记录"
        return HttpResponse(json.dumps(ret), content_type='application/json')
    
    
    ret["retcode"] = "0"
    ret["title"] = shop_info.title
    ret["name"] = shop_info.name
    ret["tel"] = shop_info.tel
    ret["sex"] = shop_info.show_sex()
    ret["email"] = shop_info.email
    ret["company"] = shop_info.company
    ret["cre_id"] = shop_info.creid

    if not shop_info.subshop_count:
        ret["subshop_count"] = "0"
    else:
        ret["subshop_count"] = shop_info.subshop_count
    
    if not shop_info.level:
        ret["level"] = "0"
    else:
        ret["level"] = shop_info.level
        
    return HttpResponse(json.dumps(ret), content_type='application/json')



#@check_login
def shop_verify_list(request):
    '''
    展示待审核的商铺申请列表
    '''
    
    apply_all = ApplyShops.objects.filter(state=0).order_by("-created_at")
    
    list_show=[]
    for item in apply_all:
        x=dict()
        x["id"] = item.id
        x["name"] = item.name
        x["sex"] = item.show_sex()
        x["tel"] = item.tel
        x["email"] = item.email
        x["company"] = item.company
        x["cre_id"] = item.creid
        x["apply_time"] = item.created_at.strftime("%Y-%m-%d")
        list_show.append(x)
        
    
    template_args = {"list_show":list_show}
    
    return render_to_response('admin_site/shop_apply.html', 
        {'template_args': template_args}, context_instance=RequestContext(request)
        )



#@check_login
def audit_shop_apply(request):
    '''
    审核的商铺申请
    '''
    ret = {}
    
    shop_id = request.GET.get("id", None)
    if not shop_id:
        ret["retcode"] = "1000"
        ret["retmsg"] = "缺少输入参数"
        return HttpResponse(json.dumps(ret), content_type='application/json')
      
    try:
        apply_record = ApplyShops.objects.get(id=shop_id, state=0)
    except ObjectDoesNotExist:
        ret["retcode"] = "1001"
        ret["retmsg"] = "未找到待审核记录"
        return HttpResponse(json.dumps(ret), content_type='application/json')
    
    res = request.GET.get("check_res", "2")
    if "1" == res:
        apply_record.state = 1
        logger.info("pass shop apply by tel %s" % apply_record.tel)
    else:
        apply_record.state = 2
        logger.info("reject shop apply by tel %s" % apply_record.tel)
    

    if "1" == res:
        ###审核通过，生成店铺数据
        new_shop = Shops()
        new_shop.name = apply_record.name
        new_shop.sex = apply_record.sex
        new_shop.tel = apply_record.tel
        new_shop.email = apply_record.email
        new_shop.creid = apply_record.creid
        new_shop.company = apply_record.company
        new_shop.title = "test"

        uuid_src = str(apply_record.id)+apply_record.tel
        uuid_value = hashlib.new("md5", uuid_src).hexdigest()
        new_shop.uuid = uuid_value
        
        logger.info("new shop uuid %s" % new_shop.uuid)
        new_shop.save()
        
        shop = Shops.objects.get(uuid=uuid_value)
        apply_record.shop = new_shop
        apply_record.save()
    else:
        apply_record.save()
    
    
    ret["retcode"] = "0"
    return HttpResponse(json.dumps(ret), content_type='application/json')




#@check_login
def shop_verify_history(request):
    '''
    展示审核历史
    '''
    
    apply_all = ApplyShops.objects.filter(state__gt=0).order_by("-created_at")
    
    list_show=[]
    for item in apply_all:
        x=dict()
        x["id"] = item.id
        x["name"] = item.name
        x["sex"] = item.show_sex()
        x["tel"] = item.tel
        x["email"] = item.email
        x["company"] = item.company
        x["cre_id"] = item.creid
        x["apply_time"] = item.created_at.strftime("%Y-%m-%d")
        x["state"] = item.state
        list_show.append(x)
        
    
    template_args = {"list_show":list_show}
    
    return render_to_response('admin_site/shop_verify_his.html', 
        {'template_args': template_args}, context_instance=RequestContext(request)
        )



#@check_login
def edit_shop(request):
    '''
    修改商铺信息
    '''

    ret = {}

    shop_id = request.POST.get("id", None)
    if not shop_id:
        ret["retcode"] = "1000"
        ret["retmsg"] = "未找到待审核记录"
        return HttpResponse(json.dumps(ret), content_type='application/json')
        
    try:
        shop_info = Shops.objects.get(id=shop_id)
    except ObjectDoesNotExist:
        ret["retcode"] = "1000"
        ret["retmsg"] = "未找到待审核记录"
        return HttpResponse(json.dumps(ret), content_type='application/json')

    title = request.POST.get("title", "")
    tel = request.POST.get("tel", "")
    email = request.POST.get("email", "")
    company = request.POST.get("company", "")
    cre_id = request.POST.get("cre_id", "")
    level = request.POST.get("level", "")
    
    if len(level) > 0:
        shop_info.title = title
        shop_info.tel = tel
        shop_info.email = email
        shop_info.creid = cre_id
        shop_info.company = company
        shop_info.level = level
    else:
        shop_info.title = title
        shop_info.tel = tel
        shop_info.email = email
        shop_info.creid = cre_id
        shop_info.company = company
        
    shop_info.save()
    ret["retcode"] = "0"
    return HttpResponse(json.dumps(ret), content_type='application/json')

        
    
