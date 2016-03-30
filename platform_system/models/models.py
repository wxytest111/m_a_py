#coding:utf8

# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from __future__ import unicode_literals

from django.db import models

from django.db.models.signals import post_save
from django.contrib.auth.models import User
from platform_system.settings import STATIC_ROOT
import logging
logger = logging.getLogger('admin_site')

class Admins(models.Model):
    # 关联现有的用户对象
    user = models.OneToOneField(User,related_name="user",verbose_name=u'用户', primary_key=True)

    ptype_state = (
        (1, u"平台用户"),
        (2, u"商户"),
    )
    ptype = models.IntegerField(choices=ptype_state,verbose_name=u'类型',default=0)

    role_state = (
        (99, u"超级管理员"),
        (1, u"系统管理员"),
    )
    role = models.IntegerField(choices=role_state,verbose_name=u'权限',default=1)

    valid_state = (
        (0, u"有效"),
        (1, u"无效"),
    )
    state = models.IntegerField(choices=valid_state,verbose_name=u'状态',default=0)

    create_time = models.DateTimeField(verbose_name=u'创建时间',db_index=True,auto_now_add=True)
    modify_time = models.DateTimeField(verbose_name=u'修改时间',blank=True,null=True,auto_now=True)

    def __str__(self):
        return self.user.username

    class Meta:
        db_table = 'admin_user'

def create_user(sender, instance, created, **kwargs):
    if created:
        if hasattr(instance,"ptype"):
            Admins.objects.create(user=instance, 
                                ptype=instance.ptype,
                                role = instance.role)

post_save.connect(create_user, sender=User)


class ApplyShops(models.Model):
    name = models.CharField(max_length=255, blank=True, null=True)
    sex = models.IntegerField(blank=True, null=True)
    tel = models.CharField(max_length=255, blank=True, null=True)
    email = models.CharField(max_length=255, blank=True, null=True)
    creid = models.CharField(max_length=255, blank=True, null=True)
    company = models.CharField(max_length=255, blank=True, null=True)
    shop = models.ForeignKey('Shops', models.DO_NOTHING, blank=True, null=True)
    
    state_choice = (
        (0, u"待审核"),
        (1, u"审核通过"),
        (2, u"已驳回"),
    )

    state = models.IntegerField(blank=True, null=True, choices=state_choice)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        managed = False
        db_table = 'apply_shops'
        
    def show_sex(self):
        if 1 == int(self.sex):
            return u"男"
        else:
            return u"女"
        

class Birds(models.Model):
    name = models.CharField(max_length=255, blank=True, null=True)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    email = models.CharField(unique=True, max_length=255)
    encrypted_password = models.CharField(max_length=255)
    reset_password_token = models.CharField(unique=True, max_length=255, blank=True, null=True)
    reset_password_sent_at = models.DateTimeField(blank=True, null=True)
    remember_created_at = models.DateTimeField(blank=True, null=True)
    sign_in_count = models.IntegerField()
    current_sign_in_at = models.DateTimeField(blank=True, null=True)
    last_sign_in_at = models.DateTimeField(blank=True, null=True)
    current_sign_in_ip = models.CharField(max_length=255, blank=True, null=True)
    last_sign_in_ip = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'birds'


class Cities(models.Model):
    name = models.CharField(max_length=255, blank=True, null=True)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'cities'





class Districts(models.Model):
    name = models.CharField(max_length=255, blank=True, null=True)
    city = models.ForeignKey(Cities, models.DO_NOTHING, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        managed = False
        db_table = 'districts'
        
        

class Customers(models.Model):
    uin = models.CharField(max_length=255, blank=True, null=True)
    passwd = models.CharField(max_length=255, blank=True, null=True)
    name = models.CharField(max_length=255, blank=True, null=True)
    sex = models.IntegerField(blank=True, null=True)
    tel = models.CharField(max_length=255, blank=True, null=True)
    address = models.CharField(max_length=255, blank=True, null=True)
    district = models.ForeignKey('Districts', models.DO_NOTHING, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        managed = False
        db_table = 'customers'

        
        

class PayRecords(models.Model):
    pay_trans = models.CharField(max_length=65, blank=True, null=True, default='')
    customer = models.ForeignKey(Customers, models.DO_NOTHING, blank=True, null=True)
    product = models.ForeignKey('Products', models.DO_NOTHING, blank=True, null=True)
    shop = models.ForeignKey('Shops', models.DO_NOTHING, blank=True, null=True)
    pay_state = models.IntegerField(blank=True, null=True)
    pay_num = models.IntegerField(blank=True, null=True)
    pay_time = models.DateTimeField(blank=True, null=True)
    total_count = models.IntegerField(blank=True, null=True)
    left_count = models.IntegerField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        managed = False
        db_table = 'pay_records'
        
    
    def show_state(self):
        if 0 == int(self.pay_state):
            return u"待付款"
        elif 1 == int(self.pay_state):
            return u"预付款"
        elif 2 == int(self,pay_state):
            return u"已付款"
        else:
            return u"已关闭"
    
import os
from uuid import uuid4
from django.utils.deconstruct import deconstructible

@deconstructible
class UploadToPathAndRename(object):

    def __init__(self, path):
        self.sub_path = path

    def __call__(self, instance, filename):
        ext = filename.split('.')[-1]
        # get filename
        if instance.pk:
            filename = '{}.{}'.format(instance.pk, ext)
        else:
            # set filename as random string
            filename = '{}.{}'.format(uuid4().hex, ext)
        # return the whole path to the file
        return os.path.join(self.sub_path, filename)

class Products(models.Model):
    name = models.CharField(verbose_name='产品名称',max_length=255, blank=True, null=True)
    description = models.TextField(verbose_name='产品描述',blank=True, null=True)
    duration = models.IntegerField(verbose_name='操作时长',blank=True, null=True)
    period = models.TextField(verbose_name='疗程周期',blank=True, null=True)
    effect = models.TextField(verbose_name='功效',blank=True, null=True)
    applicable = models.TextField(verbose_name='肤质',blank=True, null=True)

    kind_choice = (
        (1, u"脸部"),
        (2, u"颈部"),
        (3, u"身体"),
        (4, u"眼"),
        (5, u"头部"),
    )
    kind = models.IntegerField(verbose_name='产品类型',choices=kind_choice,blank=True, null=True)

    how_choice = (
        (1, u"只能使用一次"),
        (2, u"可以多次使用"),
    )
    howuse = models.IntegerField(verbose_name='产品使用类型',choices=how_choice,blank=True, null=True)
    total_count = models.IntegerField(verbose_name='可使用的总次数',blank=True, null=True)
    pic_path = models.ImageField(verbose_name='图片路径',upload_to=UploadToPathAndRename(os.path.join(STATIC_ROOT, 'images', 'products')),max_length=255, blank=True, null=True)
    show_price = models.IntegerField(verbose_name='原价，单位：分',blank=True, null=True)
    pay_price = models.IntegerField(verbose_name='支付价格，单位：分',blank=True, null=True)
    
    state_choice = (
        (1, u"草稿"),
        (2, u"发布上线"),
        (3, u"下架"),
    )
    state = models.IntegerField(verbose_name='状态',choices=state_choice, blank=True, null=True)
    admin = models.ForeignKey(Admins, blank=True, null=True)
    created_at = models.DateTimeField(verbose_name='创建时间',auto_now_add=True)
    updated_at = models.DateTimeField(verbose_name='修改时间',auto_now=True)

    class Meta:
        managed = False
        db_table = 'products'
        
    def show_howuse(self):
        if 1 == int(self.howuse):
            return u"单次使用"
        else:
            return u"多次使用"
    
        

class ShopCustomers(models.Model):
    state = models.IntegerField(blank=True, null=True)
    shop = models.ForeignKey('Shops', models.DO_NOTHING, blank=True, null=True)
    customer = models.ForeignKey(Customers, models.DO_NOTHING, blank=True, null=True)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'shop_customers'


class Shops(models.Model):
    uuid = models.CharField(max_length=255, blank=True, null=True)
    title = models.CharField(max_length=255, blank=True, null=True)
    name = models.CharField(max_length=255, blank=True, null=True)
    sex = models.IntegerField(blank=True, null=True)
    tel = models.CharField(max_length=255, blank=True, null=True)
    email = models.CharField(max_length=255, blank=True, null=True)
    creid = models.CharField(max_length=255, blank=True, null=True)
    company = models.CharField(max_length=255, blank=True, null=True)
    login_name = models.CharField(max_length=255, blank=True, null=True)
    login_pass = models.CharField(max_length=255, blank=True, null=True)
    subshop_count = models.IntegerField(blank=True, null=True)
    level = models.IntegerField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        managed = False
        db_table = 'shops'
        
    def show_sex(self):
        if 1 == int(self.sex):
            return u"男"
        else:
            return u"女"
    

class Steps(models.Model):
    number = models.IntegerField(blank=True, null=True)
    product = models.ForeignKey(Products, models.DO_NOTHING, blank=True, null=True)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'steps'


class Subscribes(models.Model):
    customer = models.ForeignKey(Customers, models.DO_NOTHING, blank=True, null=True)
    start_time = models.DateTimeField(blank=True, null=True)
    end_time = models.DateTimeField(blank=True, null=True)
    
    type_choice = (
         (1, u"主预约"),
         (2, u"子预约"),
    )

    type = models.IntegerField(blank=True, null=True, default=1, choices=type_choice)
    parent = models.IntegerField(blank=True, null=True)
    product = models.ForeignKey(Products, models.DO_NOTHING, blank=True, null=True)
    pay_record = models.ForeignKey(PayRecords, models.DO_NOTHING, blank=True, null=True)
    name = models.CharField(max_length=255, blank=True, null=True)
    sex = models.IntegerField(blank=True, null=True)
    tel = models.CharField(max_length=255, blank=True, null=True)
    district = models.ForeignKey(Districts, models.DO_NOTHING, blank=True, null=True)
    address = models.CharField(max_length=255, blank=True, null=True)
    waitress = models.ForeignKey('Waitresses', models.DO_NOTHING, blank=True, null=True)
    
    state_choice = (
         (1, u"预约中"),
         (2, u"已审核"),
         (3, u"服务人员已分配"),
         (4, u"服务中"),
         (5, u"服务完成"),
         (6, u"已取消"),
    )
    state = models.IntegerField(choices=state_choice, blank=True, default=0, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        managed = False
        db_table = 'subscribes'



class Waitresses(models.Model):
    name = models.CharField(max_length=255, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'waitresses'
