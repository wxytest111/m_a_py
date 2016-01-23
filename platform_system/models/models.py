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


class Admins(models.Model):
    # 关联现有的用户对象
    user = models.OneToOneField(User,related_name="user", primary_key=True)

    ptype_state = (
        (1, u"平台用户"),
        (2, u"商户"),
    )
    ptype = models.IntegerField(choices=ptype_state, default=0)

    create_time = models.DateTimeField(verbose_name='创建时间',db_index=True,auto_now_add=True)
    modify_time = models.DateTimeField(verbose_name='修改时间',blank=True,null=True,auto_now=True)

    class Meta:
        db_table = 'admin_user'

def create_user(sender, instance, created, **kwargs):
    if created:
        if hasattr(instance,"ptype"):
            Admins.objects.create(user=instance, 
                                ptype=instance.ptype)

post_save.connect(create_user, sender=User)


class ApplyShops(models.Model):
    name = models.CharField(max_length=255, blank=True, null=True)
    sex = models.IntegerField(blank=True, null=True)
    tel = models.CharField(max_length=255, blank=True, null=True)
    email = models.CharField(max_length=255, blank=True, null=True)
    creid = models.CharField(max_length=255, blank=True, null=True)
    company = models.CharField(max_length=255, blank=True, null=True)
    shop = models.ForeignKey('Shops', models.DO_NOTHING, blank=True, null=True)
    state = models.IntegerField(blank=True, null=True)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'apply_shops'

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


class Customers(models.Model):
    uin = models.CharField(max_length=255, blank=True, null=True)
    passwd = models.CharField(max_length=255, blank=True, null=True)
    name = models.CharField(max_length=255, blank=True, null=True)
    sex = models.IntegerField(blank=True, null=True)
    tel = models.CharField(max_length=255, blank=True, null=True)
    address = models.CharField(max_length=255, blank=True, null=True)
    district = models.ForeignKey('Districts', models.DO_NOTHING, blank=True, null=True)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'customers'


class Districts(models.Model):
    name = models.CharField(max_length=255, blank=True, null=True)
    city = models.ForeignKey(Cities, models.DO_NOTHING, blank=True, null=True)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'districts'

class PayRecords(models.Model):
    customer = models.ForeignKey(Customers, models.DO_NOTHING, blank=True, null=True)
    product = models.ForeignKey('Products', models.DO_NOTHING, blank=True, null=True)
    shop = models.ForeignKey('Shops', models.DO_NOTHING, blank=True, null=True)
    pay_state = models.IntegerField(blank=True, null=True)
    pay_num = models.IntegerField(blank=True, null=True)
    pay_time = models.DateTimeField(blank=True, null=True)
    total_count = models.IntegerField(blank=True, null=True)
    left_count = models.IntegerField(blank=True, null=True)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'pay_records'

class Products(models.Model):
    name = models.CharField(verbose_name='产品名称',max_length=255, blank=True, null=True)
    description = models.TextField(verbose_name='产品描述',blank=True, null=True)
    duration = models.IntegerField(verbose_name='单次操作时间长度',blank=True, null=True)
    period = models.TextField(verbose_name='疗程周期',blank=True, null=True)
    effect = models.TextField(verbose_name='功效',blank=True, null=True)
    applicable = models.TextField(verbose_name='适用哪些肤质',blank=True, null=True)
    kind = models.IntegerField(verbose_name='产品名称',blank=True, null=True)

    how_choice = (
        (1, u"只能使用一次"),
        (2, u"可以多次使用"),
    )
    howuse = models.IntegerField(verbose_name='产品使用类型',choices=how_choice,blank=True, null=True)
    total_count = models.IntegerField(verbose_name='可使用的总次数',blank=True, null=True)
    pic_path = models.CharField(verbose_name='图片路径',max_length=255, blank=True, null=True)
    show_price = models.IntegerField(verbose_name='原价，单位：分',blank=True, null=True)
    pay_price = models.IntegerField(verbose_name='支付价格，单位：分',blank=True, null=True)
    state_choice = (
        (1, u"草稿"),
        (2, u"发布上线"),
        (3, u"下架"),
    )
    state = models.IntegerField(verbose_name='状态',blank=True, null=True)
    admin = models.ForeignKey(Admins, models.DO_NOTHING, blank=True, null=True)
    created_at = models.DateTimeField(verbose_name='创建时间',auto_now_add=True)
    updated_at = models.DateTimeField(verbose_name='修改时间',auto_now=True)

    class Meta:
        managed = False
        db_table = 'products'

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
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'shops'


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
    product = models.ForeignKey(Products, models.DO_NOTHING, blank=True, null=True)
    pay_record = models.ForeignKey(PayRecords, models.DO_NOTHING, blank=True, null=True)
    name = models.CharField(max_length=255, blank=True, null=True)
    sex = models.IntegerField(blank=True, null=True)
    tel = models.CharField(max_length=255, blank=True, null=True)
    district = models.ForeignKey(Districts, models.DO_NOTHING, blank=True, null=True)
    address = models.CharField(max_length=255, blank=True, null=True)
    waitress = models.ForeignKey('Waitresses', models.DO_NOTHING, blank=True, null=True)
    state = models.IntegerField(blank=True, null=True)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()

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
