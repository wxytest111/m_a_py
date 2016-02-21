#coding:utf-8

from django import forms
from django.contrib.auth.models import User
from django.forms import ModelForm
from django.core.exceptions import *

error_messages = {
    'password_wrong': "密码错误",
    're_password_wrong': "两次密码不一致",
    'account_alert': "帐号异常",
    'username_not_exist': "用户不存在",
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