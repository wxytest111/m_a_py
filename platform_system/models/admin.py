from django.contrib import admin
from models import *
# Register your models here.

class AdminsAdmin(admin.ModelAdmin):
    list_display = ('user','ptype')
    ordering = ('-create_time',)
admin.site.register(Admins,AdminsAdmin)

class ProductsAdmin(admin.ModelAdmin):
    list_display = ('name','description','duration','effect','applicable','kind','howuse','total_count','show_price','pay_price','state','created_at')
    search_fields = ['name']
    ordering = ('-created_at',)
admin.site.register(Products,ProductsAdmin)
