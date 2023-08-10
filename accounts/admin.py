from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Account
# Register your models here.

# @admin.register(Account)
# class AccountAdmin(admin.ModelAdmin):
#     list_display=['id','email','username','first_name','last_name']
#     # readonly_fields=['password']

class Accountadmin(UserAdmin):
    list_display=['id','email','username','first_name','is_active']
    list_display_links=['id','email','username','first_name']
    readonly_fields=['last_login','date_joined']
    ordering=['date_joined']
    filter_horizontal=()
    list_filter=()
    fieldsets=()
    
admin.site.register(Account,Accountadmin)