from django.contrib import admin
from .models import Cart,Cart_item
# Register your models here.

@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display=['id','cart_id','date_added']
    

@admin.register(Cart_item)
class CartItemAdmin(admin.ModelAdmin):
    list_display=['id','product','cart','quantity','is_active']