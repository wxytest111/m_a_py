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
import logging
logger = logging.getLogger('admin_site')



@check_login
def admin_list(request):
    template_args = {}

    return render_to_response('admin_site/admin_list.html', 
        {'template_args': template_args}, context_instance=RequestContext(request)
        )



@check_login
def customer_list(request):
    template_args = {}

    return render_to_response('admin_site/customer_list.html', 
        {'template_args': template_args}, context_instance=RequestContext(request)
        )
