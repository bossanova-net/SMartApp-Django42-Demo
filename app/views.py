from datetime import datetime, timedelta
# Create your views to query data from ETLTransaction models. Here is an example:
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpRequest
from django.shortcuts import render, redirect, get_object_or_404
from django.core.exceptions import *
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from django.db.models import *

from app.forms import *
from app.models import *
from app.filters import *
import app.report_manager as reporter
import openpyxl
from openpyxl.utils.dataframe import dataframe_to_rows

from urllib.parse import quote
from urllib.parse import urlencode
from urllib import parse
from django.core.paginator import Paginator
import django.shortcuts as shortcuts
from django.http import HttpResponse
from app.utility import *


# from django.shortcuts import render, redirect
# from django.views.generic import CreateView, UpdateView
# from .models import Inventory, Project
# from .forms import InventoryForm
# from django.contrib import messages


def checkEmpyQueryString(request):
    listQueryParma = request.GET

    listValInParma = dict(filter(lambda elem: len(elem[1]) > 0, listQueryParma.items()))
    isNotEmplyQuery = bool(listQueryParma) and len(listValInParma) > 0
    return isNotEmplyQuery



def init_list_for_dropdownlist_inventory_form(form,brand=None, model=None):
    
    if brand is not None and model is not None:
        form.fields['brand'].queryset = brand
        form.fields['model'].queryset = model
        

"""
Create function named "manage_project" in views.py that have id(default value=0) as a parameter  to do the the following.
1. GET Methods : 
 - if it is add project then create a new "project form" defined in forms.py.
 - if it is update project then get the project by id  and take project object to "project form" defined in forms.p.
2. Post Method :
 - Get request.data from "Project Form" and Save to database
3. This funciton will return the following variables to project_manage.html 
 - All projects as queryset to "projectList" variable
 - "Project Form" to form variable
"""
# @login_required
def manage_project(request, id=0):
    if request.method == "GET":
        if id == 0:
            form = ProjectForm()
        else:
            project = get_object_or_404(Project, id=id)
            form = ProjectForm(instance=project)

    else:
        if id == 0:
            form = ProjectForm(request.POST)
            if form.is_valid():
                project = form.save()
                messages.success(request, 'Project saved successfully.')
            else:
                messages.error(request, form.errors)
        else:
            project = get_object_or_404(Project, id=id)
            form = ProjectForm(request.POST, instance=project)
            if form.is_valid():
                project = form.save()
                messages.success(request, 'Project updated successfully.')
            else:
                messages.error(request, form.errors)

    projectList = Project.objects.prefetch_related('company').all()
    
    projectFilter = ProjectFilter(request.GET, queryset=projectList)
    
    if projectFilter.form.is_valid():
        projectList = projectFilter.qs
    
    context = {'form': form, 'projectList': projectList, 'projectFilter': projectFilter}
    return render(request, 'app/project_manage.html', context)



def delete_project(request, id):
    project_obj = Project.objects.get(pk=id)

    if request.method == "GET":
        inventory_list = project_obj.inventory_set.all()

    try:
        if request.method == "POST":
            project_obj.delete()

    except Exception as ex:
        messages.ERROR(ex)

    if request.method == "GET":
        context = {'project': project_obj, 'inventoryList': inventory_list}
        return render(request, 'app/project_delete.html', context)
    else:
        return redirect('manage_project')

"""
Create function named "manage_inventory" in views.py that have id(default value=0) as a parameter  to do the the following.
1. GET Methods : 
 - if it is add inventory then create a new "inventory form" defined in forms.py.
 - if it is update inventory then get the inventory by id  and take inventory object to "inventory form" defined in forms.py.
2. Post Method :
 - Get request.data from "Inventory Form" and Save to database
3. This funciton will return the following variables to inventory_manage.html 
 - All inventory as queryset to "inventoryList" variable
 - "inventory Form" to form variable
"""

def get_brand_its_model(inventory_obj):
    if inventory_obj.model.is_active == True:
        brand_obj = Brand.objects.all()
        model_obj = Model.objects.filter(brand_id=inventory_obj.brand_id, is_active=True)
        is_active = True
    else:
        brand_obj = Brand.objects.filter(id=inventory_obj.brand_id)
        model_obj = Model.objects.filter(id=inventory_obj.model.id)
        is_active = False
    return brand_obj, model_obj
# @login_required
def manage_inventory(request, id=0):
    project = None
    isNotEmplyQuery = checkEmpyQueryString(request)
    
    inventoryList = Inventory.objects.all().prefetch_related('project','model', 'brand', 'product_type')
    
    request.session['company_query'] = request.GET.get('company')
    
    if request.method == "GET":
        if id == 0:
            form = InventoryForm()
        else:
            inventory = get_object_or_404(Inventory.objects.select_related('project'), id=id)  
            form = InventoryForm(instance=inventory)
    else:
        if id == 0:
            form = InventoryForm(request.POST)
        else:
            inventory = get_object_or_404(Inventory.objects.select_related('project'), id=id)  
            form = InventoryForm(request.POST, instance=inventory)
        
        if form.is_valid():
            inventory = form.save()
            if id == 0:
                messages.success(request, 'Inventory saved successfully.')
            else:
                messages.success(request, 'Inventory updated successfully.')
            return redirect('manage_inventory')  
        else:
            messages.error(request, form.errors)

    inventoryFilter = InventoryFilter(request.GET, queryset=inventoryList)

    # if inventoryFilter.form.is_valid():
    if inventoryFilter.qs.count() > 0  :
        inventoryList = inventoryFilter.qs
        listIDs = [x.id for x in inventoryList]
        request.session['query_inventory'] = listIDs
    else:
        inventoryList = None
        request.session['query_inventory'] = None
        
    
    context = {'form': form, 'inventoryList': inventoryList, 'project': project, 
               'inventoryFilter': inventoryFilter,'isNotEmplyQuery': isNotEmplyQuery}
    return render(request, 'app/inventory_manage.html', context)


def add_inventory(request, proj_id):

    project_obj = get_object_or_404(Project.objects.prefetch_related(
        Prefetch('inventory_set', queryset=Inventory.objects.select_related('brand', 'model', 'product_type'))
    ), id=proj_id)
    list_inventory = project_obj.inventory_set.all() #cause of many query in list
    
    if request.method == "GET":
        if len(list_inventory) == 0:
            form = InventoryForm(initial={'project': project_obj})
            init_list_for_dropdownlist_inventory_form(form)
        else:
            form = InventoryForm()

    else:
        form = InventoryForm(request.POST)
        if form.is_valid():
            inventory_obj = form.save(commit=False)
            inventory_obj.project = project_obj
            inventory_obj.save()
            messages.success(request, 'Inventory has been created successfully.')
            return redirect('add_inventory', proj_id=proj_id)
        else:
            messages.error(request, 'Error creating inventory. Please check the form.')

    
    context = {'form': form, 'project': project_obj, 'inventoryList': list_inventory, 'mode': 'new'}
    return render(request, 'app/inventory_add_new.html', context)



def update_inventory(request, id):
    inventory_obj = Inventory.objects.select_related('project__company').get(id=id)
    project_obj = inventory_obj.project
    
    if (request.method == "GET"):
        form = InventoryForm(instance=inventory_obj)        
        brand_obj, model_obj = get_brand_its_model(inventory_obj)
        init_list_for_dropdownlist_inventory_form(form, brand_obj, model_obj)
    else:
        form = InventoryForm(request.POST, instance=inventory_obj)
        init_list_for_dropdownlist_inventory_form(form)
        
        if form.is_valid():
            if form.has_changed():
                form.save()
            
                
                inventory_obj.project = project_obj
                inventory_obj.save()
                
                if next == 'close_page':
                    return HttpResponse(
                        '<script type="text/javascript">window.close(); window.parent.location.href = "/";</script>')
                else:
                    return redirect('manage_inventory')
            else:
          

                if next == 'close_page':
                    return HttpResponse(
                        '<script type="text/javascript">window.close(); window.parent.location.href = "/";</script>')
                else:
                    return redirect('manage_inventory')
        else:
            messages.error(request, form.errors)
            
    context = {}
    if request.GET.get('view_only'):
        context = {'form': form, 'project': project_obj, 'xview': 1, 'mode': 'update'}
    else:
        context = {'form': form, 'project': project_obj, 'xview': None, 'mode': 'update'}
    return render(request, 'app/inventory_update.html', context)


def delete_inventory(request, id):
    inventory_obj = Inventory.objects.get(pk=id)

    if request.method == "GET":
        inventory_obj = inventory_obj

    try:
        if request.method == "POST":
            inventory_obj.delete()

    except Exception as ex:
        messages.ERROR(ex)

    if request.method == "GET":
        context = {'inventory': inventory_obj}
        return render(request, 'app/inventory_delete.html', context)
    else:
        return redirect('manage_inventory')
    


def load_models_by_brand(request):
    brand_idx = request.GET.get('brand')
    models = Model.objects.filter(brand_id=brand_idx, is_active=True).order_by('model_name')

    return render(request, 'app/models_by_brand_list.html', {'models': models})

def export_inventory(request):
    response = export_data_refactor(request, 'query_inventory')
    return response

def export_data_refactor(request,query_session):
    
    listIDs = request.session.get(query_session, None)

    if listIDs != None:
        date_btw = ''
        buildtime = datetime.now().strftime('%d%m%y_%H%M')

        date_from = request.GET.get('date_from')
        date_to = request.GET.get('date_to')
        if date_from is not None and date_to is not None:
            date_btw = f'_From{date_from}_To{date_to}'

        company_query = request.session['company_query']

        if query_session == 'query_project' or query_session == 'query_all_project':
            df=reporter.report_project(listIDs)
            if df.empty:
                messages.error(request, "No project return")
                return render(request, 'app/export_report.html', {})
            if (company_query is not None) and (company_query != ''):
                comanpy_info=Company.objects.get(id=int(company_query ))
                file_name = f"Project_{comanpy_info.company_name}_{buildtime}.xlsx"
            else:
                file_name = f"Project_{buildtime}.xlsx"
            request.session['company_query'] = None

        elif query_session == 'query_inventory':
            df = reporter.report_inventory(listIDs)
            if df.empty:
                messages.error(request, "No inventory return except dummy inventory")
                return render(request, 'app/export_report.html', {})

            if (company_query is not None) and (company_query != ''):
                comanpy_info=Company.objects.get(id=int(company_query ))
                file_name = f"Inventory_{comanpy_info.company_name}_{buildtime}.xlsx"
            else:
                file_name = f"Inventory{date_btw}_{buildtime}.xlsx"
        # elif  query_session=='query_incident':

        df = df.fillna(value='')

        col_remove = 'ID'
        if col_remove in df.columns:
            df = df.drop([col_remove], axis=1)

        if len(df) > 0:
            try:
                wb = openpyxl.Workbook(write_only=True)
                ws = wb.create_sheet()
                for r in dataframe_to_rows(df, index=False, header=True, ):
                    ws.append(r)
            except openpyxl.utils.exceptions.IllegalCharacterError as e:
                raise e

        response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        response['Content-Disposition'] = f'attachment; filename={file_name}'


        wb.save(response)

        return response

