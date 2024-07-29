from .serializers import (TypeSerializer,CompanySerializer,PharmacySerializer,
                                ProductSerializer,StoreSerializer,Tg_usersSerializer)

from .models import (Type,Company,Product,
                     Pharmacy,Store,Tg_Users)

from rest_framework import viewsets, permissions,mixins,status

from rest_framework.decorators import action
from rest_framework.response  import Response
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from django.shortcuts import render

# Create your views here.

class Tg_usersViewSet(viewsets.GenericViewSet,mixins.CreateModelMixin,mixins.ListModelMixin,mixins.UpdateModelMixin,mixins.DestroyModelMixin,mixins.RetrieveModelMixin):
    queryset=Tg_Users.objects.all()
    serializer_class=Tg_usersSerializer

    parameters = [
        openapi.Parameter('tg_id', openapi.IN_QUERY, description='izlanishi kerak bo\'lgan ma\'lumot', type=openapi.TYPE_INTEGER),
        openapi.Parameter('is_admin', openapi.IN_QUERY, description='izlanishi kerak bo\'lgan ma\'lumot', type=openapi.TYPE_BOOLEAN),
        openapi.Parameter('is_owner', openapi.IN_QUERY, description='izlanishi kerak bo\'lgan ma\'lumot', type=openapi.TYPE_BOOLEAN),
        ]
    
    @swagger_auto_schema(manual_parameters=parameters)
    @action(detail=False,methods=['get'])

    def filter(self, request):        
        tg_id = request.query_params.get('tg_id', None)
        is_admin = request.query_params.get('is_admin', None)
        is_owner = request.query_params.get('is_owner', None)

        queryset = self.queryset

        if tg_id:
            queryset = queryset.filter(tg_id=tg_id)

        if is_admin:
            queryset = queryset.filter(is_admin=is_admin)
        
        if is_owner:
            queryset = queryset.filter(is_owner=is_owner)
        
        serializer = self.get_serializer(queryset, many=True)

        return Response(serializer.data)



class TypeViewSet(viewsets.GenericViewSet,mixins.CreateModelMixin,mixins.DestroyModelMixin,mixins.UpdateModelMixin, mixins.ListModelMixin,mixins.RetrieveModelMixin):
    queryset=Type.objects.all()
    serializer_class=TypeSerializer
    
class CompanyViewSet(viewsets.GenericViewSet,mixins.CreateModelMixin,mixins.DestroyModelMixin,mixins.UpdateModelMixin,mixins.ListModelMixin,mixins.RetrieveModelMixin):
    queryset=Company.objects.all()
    serializer_class=CompanySerializer
    
class ProductViewSet(viewsets.GenericViewSet,mixins.CreateModelMixin,mixins.DestroyModelMixin,mixins.UpdateModelMixin,mixins.ListModelMixin,mixins.RetrieveModelMixin):
    queryset=Product.objects.all()
    serializer_class=ProductSerializer
    
    parameters = [
        openapi.Parameter('name', openapi.IN_QUERY, description='izlanishi kerak bo\'lgan ma\'lumot', type=openapi.TYPE_STRING),
        openapi.Parameter('company', openapi.IN_QUERY, description='izlanishi kerak bo\'lgan ma\'lumot', type=openapi.TYPE_STRING),
        openapi.Parameter('pharma_group', openapi.IN_QUERY, description='izlanishi kerak bo\'lgan ma\'lumot', type=openapi.TYPE_STRING),
        openapi.Parameter('barcode', openapi.IN_QUERY, description='izlanishi kerak bo\'lgan ma\'lumot', type=openapi.TYPE_STRING),
        ]
    
    @swagger_auto_schema(manual_parameters=parameters)
    @action(detail=False,methods=['get'])
    
    def filter(self,request):
        name = request.query_params.get('name', None)
        company = request.query_params.get('company', None)
        pharma_group = request.query_params.get('pharma_group', None)
        barcode = request.query_params.get('barcode',None)
        
        queryset = self.queryset

        if name:
            queryset = queryset.filter(name__istartswith=name)
        
        if company:
            queryset=queryset.filter(company__name__istartswith=company)
        
        if pharma_group:
            queryset=queryset.filter(pharma_group__istartswith=pharma_group)
        
        if barcode:
            queryset=queryset.filter(barcode__istartswith=barcode)
        
        serializer = self.get_serializer(queryset, many=True)

        return Response(serializer.data)
    
    

class PharmacyViewSet(viewsets.GenericViewSet,mixins.CreateModelMixin,mixins.DestroyModelMixin,mixins.UpdateModelMixin,mixins.ListModelMixin,mixins.RetrieveModelMixin):
    queryset=Pharmacy.objects.all()
    serializer_class=PharmacySerializer
    
    parameters = [
        openapi.Parameter('name', openapi.IN_QUERY, description='izlanishi kerak bo\'lgan ma\'lumot', type=openapi.TYPE_STRING),
        openapi.Parameter('owner', openapi.IN_QUERY, description='izlanishi kerak bo\'lgan ma\'lumot', type=openapi.TYPE_STRING),
        openapi.Parameter('location', openapi.IN_QUERY, description='izlanishi kerak bo\'lgan ma\'lumot', type=openapi.TYPE_STRING),
            ]

    @swagger_auto_schema(manual_parameters=parameters)
    @action(detail=False,methods=['get']) 
    
    def filter(self,request):    
        name = request.query_params.get('name', None)
        owner = request.query_params.get('owner', None)
        location = request.query_params.get('location', None)
        queryset = self.queryset
        if name:
                queryset = queryset.filter(name__istartswith=name)
        
        if owner:
            queryset=queryset.filter(owner__tg_id=owner)
                    
        serializer = self.get_serializer(queryset, many=True)

        return Response(serializer.data)

class StoreViewSet(viewsets.GenericViewSet,mixins.CreateModelMixin,mixins.DestroyModelMixin,mixins.UpdateModelMixin,mixins.ListModelMixin,mixins.RetrieveModelMixin):
    queryset=Store.objects.all()
    serializer_class=StoreSerializer
    
    parameters = [
        openapi.Parameter('product', openapi.IN_QUERY, description='izlanishi kerak bo\'lgan ma\'lumot', type=openapi.TYPE_STRING),
        openapi.Parameter('barcode', openapi.IN_QUERY, description='izlanishi kerak bo\'lgan ma\'lumot', type=openapi.TYPE_INTEGER),
        openapi.Parameter('type_n', openapi.IN_QUERY, description='izlanishi kerak bo\'lgan ma\'lumot', type=openapi.TYPE_STRING),
        openapi.Parameter('pharmacy', openapi.IN_QUERY, description='izlanishi kerak bo\'lgan ma\'lumot', type=openapi.TYPE_STRING),
        openapi.Parameter('product_id', openapi.IN_QUERY, description='izlanishi kerak bo\'lgan ma\'lumot', type=openapi.TYPE_STRING),
        
            ]
        
    @swagger_auto_schema(manual_parameters=parameters)
    @action(detail=False,methods=['get'])
    
    def filter(self,request):
        product = request.query_params.get('product', None)
        barcode = request.query_params.get('barcode', None)
        type_n = request.query_params.get('type_n', None)
        pharmacy = request.query_params.get('pharmacy', None)
        product_id = request.query_params.get('product_id', None)
        queryset = self.queryset
        if product:
            queryset = queryset.filter(product__name__istartswith=product)
        
        if barcode:
            queryset=queryset.filter(product__barcode__istartswith=barcode)
        
        if type_n:
            queryset=queryset.filter(product__type_name__id=type_n)
        
        if pharmacy:
            queryset=queryset.filter(pharmacy__id=pharmacy)
                
        if product_id:
            queryset=queryset.filter(product__id=product_id)


        queryset=queryset.order_by('-price')

        serializer = self.get_serializer(queryset, many=True)
        
        return Response(serializer.data)