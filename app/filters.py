import django_filters

from django.utils.translation import gettext as _
from django_filters import *

from app.models import *
from app.forms  import  MyDateInput,MyDateTimeInput,MyTimeInput
from datetime import timedelta

from django.db.models import Q

import datetime as datetime
import datetime as date

#https://django-filter.readthedocs.io/en/stable/guide/usage.html
class MyEndDateFilter(django_filters.DateFilter):

    def filter(self, qs, value):
        if value:
            value = value + timedelta(1)
        return super(MyEndDateFilter, self).filter(qs, value)


def company_for_project_by_role(request):
    if request is None:
        return Company.objects.all()
    elif request.user.is_superuser:
    # elif request.user.is_staff or  request.user.is_superuser:
        return Company.objects.filter(is_customer=True)
    else:
        manager_comp= Company.objects.prefetch_related('manager').filter(manager__user=request.user,is_customer=True)
        engineer_comp=Company.objects.filter(engineer__user=request.user,is_customer=True)
        if manager_comp.count() > 0:
            return manager_comp
        elif engineer_comp.count() > 0:
            return engineer_comp
        else:
            return None
        #return Company.objects.filter( ( Q(manager__user=request.user) | Q(engineer__user=request.user)), is_customer=True)
                # next version
        # is_in_manager_group = Manager.objects.filter(user_id__exact=request.user.id,is_site_manager__exact=True).exists()
        # is_in_office_admin_group = OfficeAdmin.objects.filter(user_id__exact=request.user.id).exists()
        # return Company.objects.filter(manager__user=request.user, is_customer=is_in_manager_group,is_for_office_admin=is_in_office_admin_group)

class ProjectFilter(django_filters.FilterSet):
    company = filters.ModelChoiceFilter(queryset=company_for_project_by_role, field_name='company', label='Company')
    enq_id = django_filters.CharFilter(lookup_expr='icontains', field_name='enq_id', label='ENQ')
    project_name = django_filters.CharFilter(lookup_expr='icontains', field_name='project_name', label='Project Name')

    class Meta:
        model = Project
        fields = ['company', 'enq_id', 'project_name']


class  InventoryFilter(django_filters.FilterSet):

   company = filters.ModelChoiceFilter(queryset=company_for_project_by_role, field_name='project__company', label='Company')
   # project_title= django_filters.CharFilter(lookup_expr='icontains',field_name='project__project_name',label='Project')
# is_dummy = django_filters.BooleanFilter(field_name='is_dummy', label="Inventory-Dummy", required=True,)
   enq_id = django_filters.CharFilter(lookup_expr='icontains',  field_name='project__enq_id', label='ENQ')
#    devicename_hostname = django_filters.CharFilter(lookup_expr='icontains', field_name='devicename_hostname', label='Device/Host Name')

   product_type= django_filters.ModelChoiceFilter(queryset=Product_Type.objects.all(), field_name='product_type', label='Product-Type')
   brand = django_filters.ModelChoiceFilter(queryset=Brand.objects.all(), field_name='brand', label='Brand')

#    is_managed_by_admin=django_filters.BooleanFilter(field_name='project__company__is_managed_by_admin', label="Yes=For Admin , No=For SM", required=True)

   # customer_warranty_end__gte = django_filters.DateFilter(field_name='customer_warranty_end', lookup_expr='gte'
   #                                                   ,
   #                                                   widget=MyDateInput(format=["%Y-%m-%dT%H:%M", "%Y-%m-%d %H:%M"], ),
   #                                                   label="In-CustWarranty")

   class Meta:
     model=Inventory
     fields=['serial_number']



