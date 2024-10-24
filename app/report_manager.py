from django.db import connection
import pandas as pd
import datetime
import re

    
def report_project(listIDs):
    projectList = []
    with connection.cursor() as cursor:
        sql = """
        select
                project.id as "ID",comp.company_name  as "Customer Name" ,project.enq_id as  "ENQ",
                TO_CHAR(project.start_date, 'DD Mon YYYY') as "Start Date",
                TO_CHAR(project.end_date, 'DD Mon YYYY') as "End Date",
                
                from app_project project
                left join app_company comp on project.company_id =comp.id
                where project.is_dummy=false and project.id in %s
                order by project.enq_id
"""
        cursor.execute(sql, [tuple(listIDs)])
        # cursor.callproc('fn_list_inventory_report', (enq_id, 0, warranty_start_param, warranty_end_param))

        columns = [col[0] for col in cursor.description]
        projectList = [dict(zip(columns, row)) for row in cursor.fetchall()]
        df = pd.DataFrame(data=projectList)

    return df
def report_inventory(listIDs):
    inventoryList = []
    with connection.cursor() as cursor:
        sql = """
        select  
                inventory.id as "ID",comp.company_name  as "Customer Name" ,project.enq_id as  "ENQ",
                inventory.serial_number as  "Serial No. / CD-Key",inventory.quantity as "QTY"  ,
                 product_type.productype_name as "Type",brand.brand_name as "Brand",model.model_name as  "Model",

                TO_CHAR(inventory.customer_warranty_start,'DD Mon YYYY') as "Cust Warranty Start"
                ,TO_CHAR(inventory.customer_warranty_end,'DD Mon YYYY') as "Cust Warranty End", 
                (select sla_name from app_sla where id=inventory.sla_id ) as "SLA"
                
    from app_inventory inventory
    left join  app_project project on inventory.project_id=project.id
    left join app_company comp on project.company_id =comp.id

    left join app_product_type  product_type on inventory.product_type_id = product_type.id
    inner join  app_brand brand on inventory.brand_id =brand.id
    left join app_model model on inventory.model_id  = model.id   
    where project.is_dummy=false and inventory.id in  %s
    order by project.enq_id ,product_type.productype_name,brand.brand_name,model.model_name,inventory.serial_number
"""

        cursor.execute(sql, [tuple(listIDs)])
        # cursor.callproc('fn_list_inventory_report', (enq_id, 0, warranty_start_param, warranty_end_param))

        columns = [col[0] for col in cursor.description]
        inventoryList = [dict(zip(columns, row)) for row in cursor.fetchall()]
        df = pd.DataFrame(data=inventoryList)
        
    return df