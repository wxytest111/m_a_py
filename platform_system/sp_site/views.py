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
logger = logging.getLogger('sp_site')

# Create your views here.

def check_login(fn):
    def _check_login(*args,**kwds):
        if len(args) == 0:
            return HttpResponseRedirect(reverse("sp_site:login"))
        #已登录
        request = args[0]
        try:
            if request.user.is_anonymous():
                return HttpResponseRedirect(reverse("sp_site:login"))
            if not request.user.is_authenticated():
                return HttpResponseRedirect(reverse("sp_site:login"))

            if request.session.get("ptype") != 2:
                auth.logout(request)
                return HttpResponseRedirect(reverse("sp_site:login"))

        except Exception:
            logger.exception("login:")
            return HttpResponseRedirect(reverse("sp_site:login"))
        return fn(*args,**kwds)

    return _check_login

def login(request):
    template_args = {}
    if request.method  == "POST":
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            cd = login_form.cleaned_data
            request_user = auth.authenticate(username=cd["username"], password = cd["password"])
            auth.login(request, request_user)
            user = Admins.objects.get(user = request_user)
            request.session["ptype"] = user.ptype
            return HttpResponseRedirect(reverse("sp_site:index"))
        else:
            template_args["login_form"] = login_form
    else:
        template_args["login_form"] = LoginForm()

    return render_to_response('sp_site/login.html', 
        {'template_args': template_args}, context_instance=RequestContext(request)
        ) 

@check_login
def logout(request):
    auth.logout(request)
    #Do something cool
    return HttpResponseRedirect(reverse("sp_site:login"))

@check_login
def index(request):
    template_args = {}

    return render_to_response('sp_site/base.html', 
        {'template_args': template_args}, context_instance=RequestContext(request)
        )

@check_login
def product_manage(request):
    template_args = {}

    return render_to_response('sp_site/base.html', 
        {'template_args': template_args}, context_instance=RequestContext(request)
        )

@check_login
def product_list(request):
    template_args = {}

    return render_to_response('sp_site/base.html', 
        {'template_args': template_args}, context_instance=RequestContext(request)
        ) 

@check_login
def order_list(request):
    template_args = {}

    return render_to_response('sp_site/base.html', 
        {'template_args': template_args}, context_instance=RequestContext(request)
        )

@check_login
def change_login_pwd(request):
    template_args = {}

    return render_to_response('sp_site/base.html', 
        {'template_args': template_args}, context_instance=RequestContext(request)
        )

