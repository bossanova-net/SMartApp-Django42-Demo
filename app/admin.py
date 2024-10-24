from django.contrib import admin
from .models import  *
from django.contrib.admin import SimpleListFilter
# Register your models here.

@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    actions = None
    list_display =('company_name','is_customer','is_subcontractor','is_managed_by_admin')
    search_fields = ['company_name']
    list_filter = ['company_name']
    
@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
    actions = None
    model=Brand
    list_display = ['brand_name']
    search_fields = ['brand_name']

@admin.register(Model)
class ModelAdmin(admin.ModelAdmin):
    actions = None
    model=Model
    list_display = ['model_name', 'brand',]
    search_fields = ['model_name','brand__brand_name']
    
@admin.register(Product_Type)
class Product_TypeAdmin(admin.ModelAdmin):
    actions = None
    model=Product_Type
    list_display = ['productype_name']
    search_fields = ['productype_name']
    
@admin.register(SLA)
class  SLAAdmin(admin.ModelAdmin):
   actions = None
   def has_delete_permission(self, request, obj=None):
       return False
   
