from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import (TypeViewSet,CompanyViewSet,ProductViewSet,
                                PharmacyViewSet,StoreViewSet,Tg_usersViewSet)


router = DefaultRouter()
router.register(r'Type',TypeViewSet , basename='type')
router.register(r'Company',CompanyViewSet , basename='company')
router.register(r'Product',ProductViewSet , basename='product')
router.register(r'Pharmacy',PharmacyViewSet , basename='pharmacy')
router.register(r'Store',StoreViewSet, basename='store')
router.register(r'Telegran Users',Tg_usersViewSet, basename='telegram_users')

urlpatterns = router.urls