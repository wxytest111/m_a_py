#coding:utf-8

from django import forms
from django.contrib.auth.models import User
from django.forms import ModelForm
from django.core.exceptions import *
from models.models import *
from ckeditor.widgets import CKEditorWidget

error_messages = {
    'password_wrong': "密码错误",
    're_password_wrong': "两次密码不一致",
    'account_alert': "帐号异常",
    'username_not_exist': "用户不存在",
    'username_already_exist': "用户已存在",
}

class LoginForm(forms.Form):
    username = forms.CharField(required=True,min_length=3,max_length=16 ,label=u'用户名')
    password = forms.CharField(required=True,min_length=3,max_length=16 ,label=u'密码',widget=forms.PasswordInput)

    def clean_username(self):
        self.__user = None
        try:
            self.__user = User.objects.get(username=self.cleaned_data["username"])
        except ObjectDoesNotExist:
            raise forms.ValidationError(error_messages['username_not_exist'])
            
        return self.cleaned_data["username"]
        
    def clean_password(self):
        if self.__user:
            if not self.__user.check_password(self.cleaned_data["password"]):
                raise forms.ValidationError(error_messages['password_wrong'])
                
        return self.cleaned_data["password"]

class AdminAddForm(forms.Form):
    account = forms.CharField(required=True,min_length=4,max_length=16 ,label=u'管理员账号')
    name = forms.CharField(required=True,min_length=2,max_length=8,label=u'管理员姓名')
    password = forms.CharField(required=True,min_length=6,max_length=16 ,label=u'管理员密码',widget=forms.PasswordInput)
    re_password = forms.CharField(required=True,min_length=6,max_length=16 ,label=u'重复密码',widget=forms.PasswordInput)
    role_state = (
        (1, u"系统管理员"),
    )
    role = forms.ChoiceField(required=True,label=u'管理员类型',choices=role_state)
    
    def clean_account(self):
        self.__user = None
        try:
            self.__user = User.objects.get(username=self.cleaned_data["account"])
            raise forms.ValidationError(error_messages['username_already_exist'])
        except ObjectDoesNotExist:
            pass
            
        return self.cleaned_data["account"]

    def clean(self):
        password=self.cleaned_data.get('password')
        re_password=self.cleaned_data.get('re_password')

        if password!=re_password:
            self.add_error("re_password",u'密码两次输入不一样，请重新输入')
            #raise forms.ValidationError(u'密码两次输入不一样，请重新输入')
        return self.cleaned_data

class ChangePWDForm(forms.Form):
    old_password = forms.CharField(required=True,min_length=6,max_length=16 ,label=u'原密码',widget=forms.PasswordInput)
    password = forms.CharField(required=True,min_length=6,max_length=16 ,label=u'请输入新密码（长度8-16）',widget=forms.PasswordInput)
    re_password = forms.CharField(required=True,min_length=6,max_length=16 ,label=u'重复密码',widget=forms.PasswordInput)

    def clean_re_password(self):
        if self.cleaned_data["re_password"] != self.cleaned_data["password"]:
            raise forms.ValidationError(error_messages['re_password_wrong'])
                
        return self.cleaned_data["re_password"]


class ProductForm(ModelForm):
    description = forms.CharField(widget=CKEditorWidget(),label=u'产品描述')
    period = forms.CharField(widget=CKEditorWidget(),label=u'疗程周期')
    effect = forms.CharField(widget=CKEditorWidget(),label=u'功效')
    applicable = forms.CharField(widget=CKEditorWidget(),label=u'肤质')
    class Meta:
        model = Products

        fields = ('name','description','duration','period', 
                  'effect','applicable','kind','howuse',
                  'total_count','pic_path','show_price','pay_price',
                  'state')

