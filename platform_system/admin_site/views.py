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

import logging
logger = logging.getLogger('admin_site')

# Create your views here.

def check_login(fn):
    def _check_login(*args,**kwds):
        if len(args) == 0:
            return HttpResponseRedirect(reverse("admin_site:login"))
        #已登录
        request = args[0]
        try:
            if request.user.is_anonymous():
                return HttpResponseRedirect(reverse("admin_site:login"))
            if not request.user.is_authenticated():
                return HttpResponseRedirect(reverse("admin_site:login"))

            if request.session.get("ptype") != 1:
                auth.logout(request)
                return HttpResponseRedirect(reverse("admin_site:login"))

        except Exception:
            logger.exception("login:")
            return HttpResponseRedirect(reverse("admin_site:login"))
        return fn(*args,**kwds)

    return _check_login

def login(request):
    template_args = {}
    if request.method  == "POST":
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            cd = login_form.cleaned_data
            request_user = auth.authenticate(username=cd["username"], password = cd["password"])
            user = Admins.objects.get(user = request_user)
            if user.state == 1:
                login_form.add_error("username",u'该用户不可登陆系统')
            else:
                auth.login(request, request_user)
                request.session["ptype"] = user.ptype
                return HttpResponseRedirect(reverse("admin_site:index"))

            template_args["login_form"] = login_form
        else:
            template_args["login_form"] = login_form
    else:
        template_args["login_form"] = LoginForm()

    return render_to_response('admin_site/login.html', 
        {'template_args': template_args}, context_instance=RequestContext(request)
        ) 

@check_login
def logout(request):
    auth.logout(request)
    #Do something cool
    return HttpResponseRedirect(reverse("admin_site:login"))

@check_login
def index(request):
    template_args = {}

    return render_to_response('admin_site/base.html', 
        {'template_args': template_args}, context_instance=RequestContext(request)
        )

@check_login
def change_login_pwd(request):
    template_args = {}
    if request.method  == "POST":
        form = ChangePWDForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            if request.user.check_password(cd["old_password"]):
                request.user.set_password(cd["password"])
                request.user.save()
                template_args["state"] = "0"
            else:
                form.add_error("old_password",u'密码错误')
        template_args["form"] = form
    else:
        template_args["form"] = ChangePWDForm()
    return render_to_response('admin_site/change_pwd.html', 
        {'template_args': template_args}, context_instance=RequestContext(request)
        )
