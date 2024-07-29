from django.db import models

# Create your models here.

class Tg_Users(models.Model):
    tg_id=models.BigIntegerField(unique=True)
    is_admin=models.BooleanField()
    is_owner=models.BooleanField()
    
    
    def __str__(self)->str:
        return str(self.tg_id)
    
    class Meta:
        verbose_name='Telegram user'
        verbose_name_plural='Telegram users'



class Company(models.Model):
    name = models.CharField(max_length=250)
    origin=models.CharField(max_length=250)
    
    class Meta:
        verbose_name='Company'
        verbose_name_plural='Companies'
        ordering=['name']
        
    def __str__(self) -> str:
        
        return f'{self.name} {self.origin}'
    
    
class Type(models.Model):    
    name=models.CharField(max_length=250)
    
    class Meta:
        
        verbose_name='Type'
        verbose_name_plural='Types'
        ordering=['name']
        
    def __str__(self) -> str:
        return self.name



class Product(models.Model):
    name=models.CharField(max_length=250)
    image=models.CharField(max_length=500)
    company=models.ForeignKey(to=Company,related_name='company',on_delete=models.CASCADE)
    type_name=models.ForeignKey(to=Type,related_name='type_name',on_delete=models.CASCADE)
    pharma_group=models.CharField(max_length=250)
    description=models.TextField()
    barcode=models.CharField(max_length=13)
    validity_date=models.IntegerField()
    
    class Meta:
        
        verbose_name='Product'
        verbose_name_plural='Products'
        ordering=['name']
        
    def __str__(self) -> str:
        return f'{self.name} {self.company.origin}'
    
    
class Pharmacy(models.Model):    
    name=models.CharField(max_length=250)
    owner=models.ForeignKey(to=Tg_Users,related_name='owner',on_delete=models.CASCADE)
    location_latitute=models.CharField(max_length=50)
    location_longitude=models.CharField(max_length=50)
    contact = models.CharField(max_length=250)
    
    def __str__(self) -> str:
        return self.name
    
    class Meta:        
        verbose_name='Pharmacy'
        verbose_name_plural='Pharmacies'
        ordering=['name']

class Store(models.Model):
    pharmacy=models.ForeignKey(to=Pharmacy,related_name='pharmacy',on_delete=models.CASCADE)
    product=models.ForeignKey(to=Product,related_name='product',on_delete=models.CASCADE)
    special_code=models.CharField(max_length=50)
    price=models.IntegerField()
    
    def __str__(self) -> str:
        return self.pharmacy.name + ' ' + self.product.name
    
    class Meta:
        verbose_name='Store'
        verbose_name_plural='Stores'