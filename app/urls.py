from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from . import views
urlpatterns = [

    path('', views.manage_project, name='manage_project'),
    path('projects/<int:id>/', views.manage_project, name='manage_project'),
    path('projects/<int:proj_id>/add_inventory/', views.add_inventory, name='add_inventory'),
    path('projects/delete_project/<int:id>/', views.delete_project, name='delete_project'),
    
    path('inventories/', views.manage_inventory, name='manage_inventory'),
    path('inventories/update_inventory/<int:id>/', views.update_inventory, name='update_inventory'),
    path('inventories/delete_inventory/<int:id>/', views.delete_inventory, name='delete_inventory'),
    path('report/export_inventory/', views.export_inventory, name='export_inventory'),
    path('ajax/load-models/', views.load_models_by_brand, name='ajax_load_models'),
]