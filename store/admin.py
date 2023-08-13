from django.contrib import admin
from .models import Product,Variation
# Register your models here.

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display=['id','product_name','slug','price','stock','is_available','created_at']
    list_display_links=['id','product_name','slug']
    prepopulated_fields={'slug':('product_name',)}
    
@admin.register(Variation)
class VariationAdmin(admin.ModelAdmin):
    list_display=['id','product','variation_category','variation_value','is_active']
    
