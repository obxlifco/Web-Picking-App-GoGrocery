from webservices.models import *
from django.apps import apps
from django.http import Http404
from django.http import JsonResponse
import json
from django.db.models import * 
from rest_framework.views import APIView
from rest_framework import status
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from rest_framework.parsers import JSONParser
from datetime import datetime
from rest_framework import generics
from rest_framework.response import Response
from django.db.models import Q
from webservices.views.common import common  
#///////////////////Dynamic Delete Update
class Globalupdate(generics.ListAPIView):
    def post(self, request, format=None):
        js=request.data
        ourResult = js['table']
        table_name=ourResult['table']
        field_name=ourResult['field_name']
        value=ourResult['value']
        ourResult1 = js['data']
        model=apps.get_model('webservices',table_name)
        query = {field_name : value}
       
        for data1 in ourResult1:
            if table_name == 'EngageboostGroups' and field_name=='isdeleted':
                for data1 in ourResult1:
                    cnt = EngageboostRolemasters.objects.filter(group_id=int(data1['id']),isdeleted='n').count()    
                    if cnt == 0:
                        queryset=model.objects.filter(id=int(data1['id'])).update(**query)
                        data2 ={
                        'status':1,
                        'Message':'Successfully Deleted'
                        }
                    else:
                        data2 ={
                        'status':0,
                        'Message':'Some Group id exists in RoleMaster Table'
                        }
                return Response(data2)
            
            elif table_name == 'EngageboostShippingMasters' and field_name=='isdeleted':
                for data1 in ourResult1:
                    
                    queryset=model.objects.filter(id=int(data1['id']),shipping_type__iexact='Courier').update(**query)
                    data2 ={
                    'status':1,
                    'Message':'Successfully Deleted'
                    }
                    
                return Response(data2)
            elif table_name == 'EngageboostTrentPicklists' and field_name=='isdeleted':
                for data1 in ourResult1:
                    
                    queryset=model.objects.filter(id=int(data1['id'])).update(**query)

                    EngageboostShipmentOrders.objects.filter(trent_picklist_id=int(data1['id'])).delete()
                    EngageboostShipmentOrderProducts.objects.filter(trent_picklist_id=int(data1['id'])).delete()

                    EngageboostOrdermaster.objects.filter(trent_picklist_id=int(data1['id'])).update(trent_picklist_id=0, order_status=0)
                    EngageboostOrderProducts.objects.filter(trents_picklist_id=int(data1['id'])).update(trents_picklist_id=0, status=0)

                    data2 ={
                    'status':1,
                    'Message':'Successfully Deleted'
                    }
                    
                return Response(data2)
            elif (table_name == 'EngageboostProducts' or table_name == 'EngageboostCategoryMasters') and (field_name=='isdeleted' or field_name=='isblocked'):
                
                error = 0
                if table_name == 'EngageboostCategoryMasters':
                    if field_name == 'isdeleted' and value == 'y':
                        cat_count = model.objects.filter(parent_id=int(data1['id']),isdeleted='n').count()
                        if cat_count>0:
                            error = 1
                            data2 ={
                                'status':0,
                                'Message': 'It has child category'
                            }
                        else:
                            products = EngageboostProductCategories.objects.filter(category_id=int(data1['id']),isdeleted='n', product__isdeleted='n').values('product_id')
                            prod_count = EngageboostProducts.objects.filter(id__in=products).count()
                            # if cat_count>0 or prod_count>0:
                            if prod_count>0:
                                error = 1
                                data2 ={
                                    'status':0,
                                    'Message': 'Category already assigned to product.'
                                }
                            

                if error == 0:    
                    queryset=model.objects.filter(id=int(data1['id'])).update(**query)

                    if field_name == 'isdeleted' and value == 'y':
                        
                        if table_name == 'EngageboostProducts':
                            EngageboostProductStocks.objects.filter(product_id=int(data1['id'])).update(real_stock=0)
                            EngageboostCossSellProducts.objects.filter(Q(product_id=int(data1['id']))|Q(cross_product_id=int(data1['id']))).delete()
                        
                        data2 ={
                            'status':1,
                            'Message': 'Successfully Deleted'
                            }
                    elif field_name == 'isblocked' and value == 'y':
                        data2 ={
                            'status':1,
                            'Message': 'Successfully Blocked'
                            }
                    elif field_name == 'isblocked' and value == 'n':
                        data2 ={
                            'status':1,
                            'Message': 'Successfully Unblocked'
                            }
                    else:
                        data2 ={
                            'status':0,
                            'Message': 'Invalid Request Sent'
                            } 
                
                if error == 0:
                    elastic = common.change_field_value_elastic(int(data1['id']),table_name,{field_name:value})           
            elif (table_name == 'EngageboostWarehouseMasters'):
                queryset=model.objects.filter(id=int(data1['id'])).update(**query)
                if field_name == 'isdeleted' and value == 'y':
                    data2 ={
                        'status':1,
                        'Message': 'Successfully Deleted'
                    }
                    # data_id = int(data1['id'])
                    # ProductElasticUpdate(data_id)
            else:    
                queryset=model.objects.filter(id=int(data1['id'])).update(**query)
                if field_name == 'isdeleted' and value == 'y':
                    data2 ={
                        'status':1,
                        'Message': 'Successfully Deleted'
                        }
                elif field_name == 'isblocked' and value == 'y':
                    data2 ={
                        'status':1,
                        'Message': 'Successfully Blocked'
                        }
                elif field_name == 'isblocked' and value == 'n':
                    data2 ={
                        'status':1,
                        'Message': 'Successfully Unblocked'
                        }
                else:
                    data2 ={
                        'status':0,
                        'Message': 'Invalid Request Sent'
                        }

                # if table_name == 'EngageboostDiscountMasters':
                #     objproduct_list = EngageboostDiscountMastersConditions.objects.filter(discount_master_id = int(data1['id'])).values_list('all_product_id',flat=True)
                #     if objproduct_list :
                #         for elastic_product_id in objproduct_list:
                #             if(elastic_product_id is not None):
                #                 print('Hello', elastic_product_id)
                #                 if("," in elastic_product_id):
                #                     prod_lst = elastic_product_id.split(",")
                #                     elastic = common.update_bulk_elastic('EngageboostProducts',prod_lst)
                #                 else:
                #                     elastic = common.update_bulk_elastic('EngageboostProducts',[int(elastic_product_id)])
                if data2['status']==1:
                    common.related_products_to_elastic(table_name,int(data1['id']))  

        return Response(data2)




class Active(APIView):
    def get(self, request, format=None):
        settings = EngageboostProducts.objects.filter(isdeleted='n').count()
        data = {
        'active':settings 
        }
        return JsonResponse(data)

    def put(self, request, format=None):
        settings = EngageboostProducts.objects.filter(isdeleted='y').count()
        data = {
        'active':settings 
        }
        return JsonResponse(data)

    def post(self, request, format=None):
        settings = EngageboostProducts.objects.filter().count()
        data = {
        'active':settings 
        }
        return JsonResponse(data)