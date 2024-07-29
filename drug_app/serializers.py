from rest_framework.serializers import ModelSerializer
from .models import (Type,Company,Product,
                     Pharmacy,Store,Tg_Users)


class TypeSerializer(ModelSerializer):

    class Meta:
        model=Type
        fields='__all__'

class Tg_usersSerializer(ModelSerializer):

    class Meta:
        model=Tg_Users
        fields='__all__'

class CompanySerializer(ModelSerializer):

    class Meta:
        model=Company
        fields='__all__'


class PharmacySerializer(ModelSerializer):
    class Meta:
        model=Pharmacy
        fields='__all__'
        
    def to_representation(self, instance):
        response=super().to_representation(instance)
        response['id']=instance.id
        response['name']=instance.name
        response['owner']=instance.owner.tg_id
        response['location_latitute']=instance.location_latitute
        response['location_longitude']=instance.location_longitude
        response['contact']=instance.contact
        
        return response

class ProductSerializer(ModelSerializer):
    class Meta:        
        model=Product
        fields=['id','name', 'image', 'company','type_name','pharma_group','description','barcode','validity_date']
        
    def to_representation(self, instance):
        response=super().to_representation(instance)
        response['id']=instance.id
        response['name']=instance.name
        response['image']=instance.image
        response['company']=[instance.company.name, instance.company.origin]
        response['type_name']=instance.type_name.name
        response['pharma_group']=instance.pharma_group
        response['description']=instance.description
        response['barcode']=instance.barcode
        response['validity_date']=instance.validity_date
        
        return response
        

class StoreSerializer(ModelSerializer):
    class Meta:
        model=Store
        fields='__all__'
    
    def to_representation(self, instance):
        response=super().to_representation(instance)
        response['id']=instance.id
        response['pharmacy']=instance.pharmacy.name
        response['product']=[instance.product.name, instance.product.id, instance.product.image]
        response['special_code']=instance.special_code
        response['type_name']=[instance.product.type_name.name, instance.product.type_name.id]
        return response