#coding:utf8
from django.shortcuts import render_to_response
from django.template import  RequestContext
from django.contrib.auth.models import User
from django.http import HttpResponse,HttpResponseRedirect
from django.contrib import auth
from django.core.urlresolvers import reverse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q
from forms import *
from models.models import *
from views import check_login
from comm import *
from platform_system.settings import DOWNLOAD_FILE_DIR

import json
import hashlib
from datetime import datetime
import time

import logging
logger = logging.getLogger('admin_site')





@check_login
def subc_list(request):
    '''
    查询主预订列表
    '''
    template_args = {}
    

    if "application/json" in request.META["HTTP_ACCEPT"]:

        start = int(request.POST.get("start"))
        length = int(request.POST.get("length"))
        key = request.POST.get("search[value]")
        order_req = request.POST.get("columns[3][orderable]")

        ###query major subc list
        subc_list = Subscribes.objects.filter(type=1)
        if key:
            subc_list = subc_list.filter(Q(customer__name__contains=key)|Q(customer__tel__contains=key))

        total_count = subc_list.count()

 
        if order_req == 'true' and request.POST.get("order[0][column]") == "3" and request.POST.get("order[3][dir]") == "asc":
            subc_list = subc_list.order_by("created_at")
        else:
            subc_list = subc_list.order_by("-created_at")


        subc_list = subc_list[start:start+length]
            
        template_args["draw"] = int(request.POST.get("draw","0"))
        template_args["recordsTotal"] = int(total_count)
        template_args["recordsFiltered"] = int(total_count)
        template_args["data"] = []


        for subc in subc_list:
            x = {}
            x["id"] = subc.id
            x["name"] = subc.name
            x["sex"] = subc.sex
            x["tel"] = subc.tel
            x["addr"] = subc.address
            x["start_time"] = subc.start_time.strftime("%Y-%m-%d %H:%M:%S")
            x["end_time"] = subc.end_time.strftime("%Y-%m-%d %H:%M:%S")
            x["state"] = subc.state
            x["waitress"] = subc.waitress.name
            x["create_at"] = subc.created_at.strftime("%Y-%m-%d")

            template_args["data"].append(x)

        return HttpResponse(json.dumps(template_args), content_type='application/json')
    else:
        return render_to_response('admin_site/subc_list.html', 
            {'template_args': template_args}, context_instance=RequestContext(request)
            )
        
       
       
@check_login    
def query_waitress_list(request):
    '''
    查询服务生列表 
    '''
    
    ret={}
    
    waitress_all = Waitresses.objects.filter();
    list_all=[]
    for person in waitress_all:
        x={}
        x["id"] = person.id
        x["name"] = person.name
        list_all.append(x)
       
    ret["waitress_list"] = list_all
    ret["retcode"] = "0"
    return HttpResponse(json.dumps(ret), content_type='application/json')
        
    
    
       
@check_login 
def query_child_subc_list(request):
    '''
    查询主预约下的具体产品预约
    '''
    
    ret = {}
    
    parent_id = request.GET.get("id", "-1");
    subc_list = Subscribes.objects.filter(type=2);
    subc_list = subc_list.filter(parent=parent_id);
    
    total_count = subc_list.count()
    list_prod = []
    for subc in subc_list:
        x={}
        x["id"] = subc.id
        x["p_name"] = subc.product.name
        x["type"] = subc.product.howuse
        x["total_num"] = subc.product.total_count
        x["left_num"] = subc.pay_record.left_count
        list_prod.append(x)
        
    ret["retcode"] = "0"
    ret["prod_list"] = list_prod
    ret["prod_num"] = str(total_count)
    return HttpResponse(json.dumps(ret), content_type='application/json')
    


@check_login
def edit_subc(request):
    '''
    编辑预订信息
    '''
    
    
    ret = {}

    subc_id = request.POST.get("id", "-1")
    try:
        major_subc = Subscribes.objects.get(id=subc_id)
    except ObjectDoesNotExist:
        ret["retcode"] = "1001"
        ret["retmsg"] = "未找到记录"
        return HttpResponse(json.dumps(ret), content_type='application/json')


    tel = request.POST.get("tel", "")
    addr = request.POST.get("addr", "")
    start_time = request.POST.get("start_time", "")
    end_time = request.POST.get("end_time", "")
    waitress_id = request.POST.get("waitress", "1")
    state = request.POST.get("state", "1")
    
    ###参数检查
    
    ###保存数据
    major_subc.tel = tel
    major_subc.address = addr
    logger.info("start_time:%s end_time:%s" % (start_time,end_time))
    major_subc.waitress = Waitresses.objects.get(id=waitress_id )
    major_subc.start_time = datetime.strptime(start_time, "%Y-%m-%d %H:%M:%S")
    major_subc.end_time = datetime.strptime(end_time, "%Y-%m-%d %H:%M:%S")
    major_subc.state = state
    major_subc.save()

    ret["retcode"] = "0"
    return HttpResponse(json.dumps(ret), content_type='application/json')

        
@check_login
def order_list(request):
    '''
    查询订单记录
    '''
    
    template_args = {}
    if "application/json" in request.META["HTTP_ACCEPT"]:

        start = int(request.POST.get("start"))
        length = int(request.POST.get("length"))
        key = request.POST.get("search[value]")
        paytime_sort = request.POST.get("columns[8][orderable]")
        createtime_sort = request.POST.get("columns[11][orderable]")
    
        payorder_all = PayRecords.objects.filter()
        if key :
            payorder_all = payorder_all.filter(Q(customer__name__contains=key)|Q(customer__tel__contains=key))
    
        total_count = payorder_all.count()
    
        if paytime_sort == 'true' and request.POST.get("order[0][column]") == "8" and request.POST.get("order[0][dir]") == "asc":
            payorder_all = payorder_all.order_by("pay_time")
        else:
            payorder_all = payorder_all.order_by("-pay_time")
            
        if createtime_sort == 'true' and request.POST.get("order[0][column]") == "11" and request.POST.get("order[0][dir]") == "asc":
            payorder_all = payorder_all.order_by("created_at")
        else:
            payorder_all = payorder_all.order_by("-created_at")

    
            payorder_all = payorder_all[start:start+length]
                
        template_args["draw"] = int(request.POST.get("draw","0"))
        template_args["recordsTotal"] = int(total_count)
        template_args["recordsFiltered"] = int(total_count)
        template_args["data"] = []
    

        for pay_order in payorder_all:
            x = {}
            x["payuser_id"] = pay_order.customer.id
            x["name"] = pay_order.customer.name
            x["tel"] = pay_order.customer.tel
            x["pt_id"] = pay_order.product.id
            x["pt_name"] = pay_order.product.name
            x["pt_price"] = transfer_fen_2_yuan(pay_order.product.pay_price)
            x["paynum"] = transfer_fen_2_yuan(pay_order.pay_num)
            x["paystate"] = pay_order.pay_state
            x["paytime"] = pay_order.pay_time.strftime("%Y-%m-%d %H:%M:%S")
            x["total_count"] = pay_order.total_count
            x["left_count"] = pay_order.left_count
            x["create_at"] = pay_order.created_at.strftime("%Y-%m-%d %H:%M:%S")
            x["id"] = pay_order.id
            template_args["data"].append(x)
    
        return HttpResponse(json.dumps(template_args), content_type='application/json')
    else:
        return render_to_response('admin_site/order_list.html', 
            {'template_args': template_args}, context_instance=RequestContext(request)
            )
    

@check_login
def edit_order(request):
    '''
    修改订单信息
    '''
    
    ret = {}
    
    payorder_id = request.POST.get("id", "-1")
    try:
        pay_order = PayRecords.objects.get(id=payorder_id)
    except ObjectDoesNotExist:
        ret["retcode"] = "1001"
        ret["retmsg"] = "未找到订单"
        return HttpResponse(json.dumps(ret), content_type='application/json')
    

    pay_num = request.POST.get("paynum", "-1")
    if 1 == check_input_price(pay_num):
        ret["retcode"] = "1002"
        ret["retmsg"] = "订单支付金额格式错误"
        return HttpResponse(json.dumps(ret), content_type='application/json')
        
    
    pay_state = request.POST.get("state", "99")
    pay_order.pay_num = transfer_yuan_2_fen(pay_num)
    pay_order.pay_state = pay_state
    if pay_state == 2 and pay_order.pay_num != pay_order.product.pay_price:
        ret["retcode"] = "1003"
        ret["retmsg"] = "支付金额与商品价格不一致"
        return HttpResponse(json.dumps(ret), content_type='application/json')
        
    pay_order.save()
    
    ret["retcode"] = "0"
    return HttpResponse(json.dumps(ret), content_type='application/json')





@check_login
def download_payorder_list(request):
    '''
    下载所有订单
    '''
    
    filename = "pay_order.xlsx"
    
    ###创建文件
    excel_work,excel_sheet = create_exel("order", filename, 7)
    ###生成文件头行
    add_order_top_to_exel(excel_work, excel_sheet)
    
    ###填充数据
    start_time = request.GET.get("start_time")
    end_time = request.GET.get("end_time")
    pay_order_list = PayRecords.objects.filter(created_at__range=(start_time,end_time))
    pay_order_list.filter(pay_state__range=(1,2))
    count = 1
    for x in pay_order_list:
        y=[]
        y.append(x.customer.name)
        y.append(x.customer.tel)
        if 1 == x.customer.sex:
            y.append(u"男")
        else:
            y.append(u"女")
        y.append(x.product.name)
        y.append(transfer_fen_2_yuan(x.pay_num))
        y.append(x.show_state())
        y.append(x.pay_time.strftime("%Y-%m-%d"))
        add_row_to_exel(excel_work, excel_sheet, count, y)
        count +=1
    
    
    ###关闭文件
    excel_work.close()
    file_path = DOWNLOAD_FILE_DIR + "/order/" + filename
   
    f = open(file_path)
    data = f.read()
    f.close()
    
    response = HttpResponse(data, content_type='application/octet-stream') 
    response['Content-Disposition'] = 'attachment; filename=%s' % filename
 
    return response
    
    

@check_login
def prod_simple_detail(request):
    '''
    商品简要信息查询
    '''
    
    ret = {}
    p_id = request.GET.get("id")
    try:
        p_info = Products.objects.get(id=p_id)
    except ObjectDoesNotExist:
        ret["retcode"] = "1001"
        ret["retmsg"] = "未找到指定产品"
        return HttpResponse(json.dumps(ret), content_type='application/json')

    ret["retcode"] = "0"
    ret["name"] = p_info.name
    ret["how_use"] = p_info.show_howuse()
    ret["total_count"] = p_info.total_count
    ret["pay_price"] = transfer_fen_2_yuan(p_info.pay_price)
    return HttpResponse(json.dumps(ret), content_type='application/json')



@check_login
def download_subc_list(request):
    '''
    下载预约记录
    '''
    
    filename = "subc_list.xlsx"
    
    ###创建文件
    excel_work,excel_sheet = create_exel("subc", filename, 7)
    ###生成文件头行
    add_subc_top_to_exel(excel_work, excel_sheet)
    
    ###填充数据
    start_time = request.GET.get("start_time")
    end_time = request.GET.get("end_time")
    qry_state = request.GET.get("state", "2")

    subc_list = Subscribes.objects.filter(created_at__range=(start_time,end_time))
    subc_list = subc_list.filter(type=1)
    
    if "1" == qry_state:
        qry_state = "5"
        subc_list.filter(state=qry_state)
        
    count = 1
    for x in subc_list:
        y=[]
        y.append(x.waitress.name)
        y.append(x.customer.name)
        y.append(x.customer.tel)
        if 1 == x.customer.sex:
            y.append(u"男")
        else:
            y.append(u"女")
        y.append(x.start_time.strftime("%Y-%m-%d %H:%M:%S"))
        y.append(x.end_time.strftime("%Y-%m-%d %H:%M:%S"))
        y.append(x.get_state_display())
        add_row_to_exel(excel_work, excel_sheet, count, y)
        count +=1
    
    
    ###关闭文件
    excel_work.close()
    file_path = DOWNLOAD_FILE_DIR + "/subc/" + filename
   
    f = open(file_path)
    data = f.read()
    f.close()
    
    response = HttpResponse(data, content_type='application/octet-stream') 
    response['Content-Disposition'] = 'attachment; filename=%s' % filename
 
    return response
