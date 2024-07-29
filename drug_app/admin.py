from django.contrib import admin
from .models import (Type,Company,Product,
                        Pharmacy,Store,Tg_Users)

@admin.register(Tg_Users)
class Tg_UsersAdmin(admin.ModelAdmin):
    list_display=['tg_id']
@admin.register(Type)
class TypeAdmin(admin.ModelAdmin):
    list_display=['id','name']
    search_fields=['name']

@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    list_display=['id','name','origin']

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display=['id','name','company','type_name','pharma_group','barcode','validity_date']
    search_fields=['name','barcode','company']
    
    


@admin.register(Pharmacy)
class PharmacyAdmin(admin.ModelAdmin):
    list_display=['id','name','owner','contact']
    search_fields=['name']
    
    def owner(self,object): return object.tg_id

@admin.register(Store)
class StoreAdmin(admin.ModelAdmin):
    list_display=['id','pharmacy','product','special_code','price']
    search_fields=['product','special_code']
    

