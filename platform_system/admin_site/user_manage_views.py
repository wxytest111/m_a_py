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

from forms import *
from models.models import *
from views import check_login
import json
import logging
logger = logging.getLogger('admin_site')

@check_login
def admin_list(request):
    template_args = {}
    if "application/json" in request.META["HTTP_ACCEPT"]:
        start = int(request.GET["start"])
        length = int(request.GET["length"])
        key = request.GET.get("search[value]")
        order_desc = request.GET.get("columns[4][orderable]")

        admin_list = Admins.objects.filter(role=1,ptype=1)
        if key :
            admin_list = admin_list.filter(Q(user__username__contains=key)|Q(user__first_name__contains=key))

        total_count = admin_list.count()

        if order_desc == 'true' and request.GET.get("order[0][column]") == "4" and request.GET.get("order[0][dir]") == "asc":
            admin_list = admin_list.order_by("user__last_login")
        else:
            admin_list = admin_list.order_by("-user__last_login")

        admin_list = admin_list[start:start+length]
                
        template_args["draw"] = int(request.GET.get("draw","0"))
        template_args["recordsTotal"] = int(total_count)
        template_args["recordsFiltered"] = int(total_count)
        template_args["data"] = []

        for admin in admin_list:
            x = {}
            x["id"] = admin.user.id
            x["username"] = admin.user.username
            x["firstname"] = admin.user.first_name
            x["display_role"] = admin.get_role_display()
            x["state"] = admin.state
            x["display_state"] = admin.get_state_display()
            x["last_login"] = None if not admin.user.last_login else admin.user.last_login.strftime("%Y-%m-%d %H:%M:%S")

            template_args["data"].append(x)

        return HttpResponse(json.dumps(template_args), content_type='application/json')
    else:
        return render_to_response('admin_site/admin_list.html', 
            {'template_args': template_args}, context_instance=RequestContext(request)
            )


@check_login
def admin_add(request):
    template_args = {}

    if request.method  == "POST":
        form = AdminAddForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            newuser = User()
            newuser.username = cd["account"]
            newuser.first_name = cd["name"]
            newuser.ptype = 1
            newuser.role = 1
            newuser.set_password(cd["password"])
            newuser.is_staff = 0
            newuser.save()

            return HttpResponseRedirect(reverse("admin_site:admin_list"))

        template_args["form"] = form
    else:
        template_args["form"] = AdminAddForm()

    return render_to_response('admin_site/admin_add.html',
        {'template_args': template_args}, context_instance=RequestContext(request)
        )

@check_login
def unuse_admin(request):
    template_args = {}

    uid = request.GET["id"]
    try:
        op = request.GET.get("action","2")
        admin = Admins.objects.get(role=1,user__id = uid)
        if op == "1": #启用
            admin.state = 0
        else:
            admin.state = 1
        admin.save()

        template_args["retcode"] = "0"
        template_args["retmsg"] = "success"
    except ObjectDoesNotExist:
        template_args["retcode"] = "-1"
        template_args["retmsg"] = "用户不存在"
    
    return HttpResponse(json.dumps(template_args), content_type='application/json')

@check_login
def customer_list(request):
    template_args = {}

    return render_to_response('admin_site/customer_list.html', 
        {'template_args': template_args}, context_instance=RequestContext(request)
        )
