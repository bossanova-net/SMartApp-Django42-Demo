from django.db import models
from datetime import datetime
from django.contrib.auth.models import  User


class Company(models.Model):
    company_name = models.CharField('Company Name', max_length=255,unique=True )

    is_customer =models.BooleanField('Is Customer',default=True)
    is_subcontractor = models.BooleanField('Is Sub Contractor', default=False)
    is_managed_by_admin=models.BooleanField('Is Managed By Admin', default=False)

    def __str__(self):
        return f'{self.company_name}'

    class Meta:
        ordering = ['company_name']






class Project(models.Model):
    enq_id=models.CharField('ENQ',max_length=100,unique=True)
    project_name=models.CharField('Project Name',max_length=255)

    company=models.ForeignKey(Company,on_delete=models.CASCADE)
    is_dummy=models.BooleanField("Is Dummy" ,default=False)

    project_start = models.DateField( verbose_name= 'Project-Start')
    project_end = models.DateField(verbose_name= 'Project-End')

    updated_at = models.DateTimeField(auto_now=True, verbose_name="Update At")


    def __str__(self):
        return self.enq_id
    class Meta:
        ordering = ['enq_id']
        

# generate Models.py from detail below
#     create the django model named "Brand" consist of the following columns.
#     - brand_name as string type and unique and ordering by 'brand_name'

#     create the django model named "Model" consist of the following columns.
#     - model_name as string type and ordering by 'model_name'
#     - brand as foreign key of Brand model
    
#     create the django model named "Product_Type" consist of the following columns.
#     - productype_name as string type and ordering by 'productype_name'
    
#     create the django model named "SLA" consist of the following columns.
#     - sla_name as string type 
    
#     create the django model named "Inventory" consist of the following columns.
#     - serial_number as string type and ordering by 'serial_number'
#     - quantity as string type and ordering by 'quantity'
#     - brand as foreign key of Brand model
#     - model as foreign key of Model model
#     - product_type as foreign key of Product_Type model
#     - customer_warranty_start as date type
#     - customer_warranty_end as date type
#     - sla as foreign key of SLA model


class Brand(models.Model):
    brand_name=models.CharField(max_length=100,unique=True)
    def __str__(self):
        return self.brand_name

    class Meta:
        ordering = ['brand_name']


class Model(models.Model):
    model_name=models.CharField(max_length=100)
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE)
    def __str__(self):
        # return f'{self.brand.brand_name} - {self.model_name}'
        return self.model_name
    class Meta:
        ordering = ['model_name']

    def __str__(self):
        return f'{self.model_name} - {self.brand.brand_name}'

class Product_Type(models.Model):
    productype_name = models.CharField(max_length=255)
    def __str__(self):
        return self.productype_name
    class Meta:
        ordering = ['productype_name']


class SLA(models.Model):
    sla_name = models.CharField(max_length=255)
    def __str__(self):
        return self.sla_name


class Inventory(models.Model):
    
    project = models.ForeignKey(Project, on_delete=models.CASCADE, null=True, blank=True)

    serial_number = models.CharField('Serial Number', max_length=255, unique=True)
    quantity = models.IntegerField('Quantity')
    product_type=models.ForeignKey( Product_Type,on_delete=models.CASCADE,verbose_name='Product Type')
    brand=models.ForeignKey( Brand,on_delete=models.CASCADE,verbose_name='Brand')
    model = models.ForeignKey( Model, on_delete=models.CASCADE,verbose_name='Model')
    customer_warranty_start = models.DateField('Customer Warranty Start')
    customer_warranty_end = models.DateField('Customer Warranty End')
    sla = models.ForeignKey(SLA, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.serial_number} - {self.quantity}'

    class Meta:
        ordering = ['serial_number']

    