from webservices.models import EngageboostMarketplaceFieldValue,EngageboostDefaultsFields,EngageboostDefaultModuleLayoutFields,EngageboostProductCategories,EngageboostCossSellProducts,EngageboostRelatedProducts,EngageboostProducts,EngageboostGridLayouts,EngageboostGridColumnLayouts
from django.http import Http404
from webservices.serializers import CossSellProductsSerializer,RelatedProductsSerializer,BasicinfoSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from rest_framework.parsers import JSONParser
from datetime import datetime
from rest_framework import generics
from itertools import chain
from django.core import serializers
from django.http import HttpResponse
from django.db.models import Q                  
from webservices.views import loginview
import sys
import traceback
from webservices.views.common import common
   
class RelatedProductList(generics.ListAPIView):
# """ List all Products """
	def get_object(self, product_id):
		company_db = loginview.db_active_connection(request)
		try:
			return EngageboostRelatedProducts.objects.using(company_db).get(product_id=product_id)
		except EngageboostRelatedProducts.DoesNotExist:
			raise Http404

	def get(self, request, product_id,product_type, format=None,partial=True):
		company_db = loginview.db_active_connection(request)
		user = EngageboostRelatedProducts.objects.using(company_db).all().filter(product_id=product_id,related_product_type=product_type)
		serializer = RelatedProductsSerializer(user,many=True)
		user1 = EngageboostProducts.objects.using(company_db).all().filter(isblocked='n',isdeleted='n')
		serializer1 = BasicinfoSerializer(user1,many=True)
		if(serializer): 
			data ={
				'status':1,
				'api_status':serializer.data,
				'message':'Data Found',
				}
		else:
			data ={
				'status':0,
				'api_status':serializer.errors,
				'message':'Data Not Found',
				}
		return Response(data)

# Insert new related product 
	
	def post(self, request, format=None,many=True):
		company_db = loginview.db_active_connection(request)
		has_multy=request.data

		try:
			for data1 in has_multy:
				Reviews = EngageboostRelatedProducts.objects.using(company_db).filter(product_id=data1['product_id'],related_product_type=data1['related_product_type']).delete()
				for data1 in has_multy:
					if int(data1['related_product_id']) != 0:
						serializer = RelatedProductsSerializer(data=data1)
						if serializer.is_valid():
							serializer.save()
							data ={
								'status':1,
								'message':'Successfully Updated',
								}
						else:
							data ={
									'status':0,
									'errors':serializer.errors,
									'message':'Data Not Found',
									}
					else:
						data = {
							'status': 1,
							'message': 'Successfully Updated',
						}
		except Exception as error:
			trace_back = sys.exc_info()[2]
			line = trace_back.tb_lineno
			data = {"status":0,"api_status":traceback.format_exc(),"error_line":line,"error_message":str(error),"message": str(error)}            
		return Response(data)

			
			
class RelatedProductSet(generics.ListAPIView):
# """ List all Edit,Uodate Brand """
	def get_object(self, product_id):
		company_db = loginview.db_active_connection(request)
		try:
			return EngageboostRelatedProducts.objects.using(company_db).get(product_id=product_id)
		except EngageboostRelatedProducts.DoesNotExist:
			raise Http404

	def post(self, request, format=None,many=True):
		company_db = loginview.db_active_connection(request)
		product_id=request.data.get('product_id')
		user = EngageboostRelatedProducts.objects.using(company_db).all().filter(product_id=product_id)
		serializer = RelatedProductsSerializer(user,many=True)
		#####################Query Generation#################################
		if request.data.get('search') and request.data.get('order_by'):
			key=request.data.get('search')
			order_by=request.data.get('order_by')
			order_type=request.data.get('order_type')
			if(order_type=='+'):
				order=order_by
			else:
				order='-'+order_by
			result = EngageboostProducts.objects.using(company_db).all().order_by(order).filter(Q(name__icontains=key)|Q(sku__icontains=key)|Q(visibility_id__icontains=key)|Q(cost_per_unit__icontains=key)|Q(default_price__icontains=key))
		elif request.data.get('search'):
			key=request.data.get('search')
			result = EngageboostProducts.objects.using(company_db).all().order_by('-id').filter(Q(name__icontains=key)|Q(sku__icontains=key)|Q(visibility_id__icontains=key)|Q(cost_per_unit__icontains=key)|Q(default_price__icontains=key))
		elif request.data.get('order_by'):
			order_by=request.data.get('order_by')
			order_type=request.data.get('order_type')
			if(order_type=='+'):
				order=order_by
			else:
				order='-'+order_by
			result = EngageboostProducts.objects.using(company_db).all().order_by(order)    
		else:
			result = EngageboostProducts.objects.using(company_db).all().order_by('-id')
		result=result.filter(~Q(id=product_id)).filter(isblocked='n',isdeleted='n')
		page = self.paginate_queryset(result)
		#####################Query Generation#################################
		#####################Layout#################################
		if page is not None:
			serializer_product = BasicinfoSerializer(page, many=True)
			module='Products'
			screen_name='list_related'
			layout_fetch=EngageboostGridLayouts.objects.using(company_db).get(module=module,screen_name=screen_name)
			layout_header=layout_fetch.header_name.split("@@")
			layout_field=layout_fetch.field_name.split("@@")
			layout_check=EngageboostGridColumnLayouts.objects.using(company_db).filter(module=module,screen_name=screen_name).count()
			layout={}
			layout_arr=[]

			for header,field in zip(layout_header,layout_field):
				ex_layout_field=field.split(".")
				field_name=ex_layout_field[0]
				if len(ex_layout_field)>1:
					child_name=ex_layout_field[1]
				else:
					child_name=''

				if(layout_check):
					layout_column_fetch=EngageboostGridColumnLayouts.objects.using(company_db).get(module=module,screen_name=screen_name)
					layout_column_header=layout_column_fetch.header_name
					layout_column_field=layout_column_fetch.field_name

					if header in layout_column_header:
						status=1
					else:
						status=0
				else:
					status=1        
				layout={"title":header,"field":field_name,"child":child_name,"show":status}
				layout_arr.append(layout)
			
		#####################Layout################################# 

		##################Applied Layout#####################   
		if(layout_check):
			layout_column_check=EngageboostGridColumnLayouts.objects.using(company_db).get(module=module,screen_name=screen_name)
			layout_header2=layout_column_check.header_name.split("@@")

			layout_header3 = list(set(layout_header) - set(layout_header2))
			layout_header = layout_header2+layout_header3

			layout_field2=layout_column_check.field_name.split("@@")

			layout_field3 = list(set(layout_field) - set(layout_field2))
			layout_field = layout_field2+layout_field3

		layout2={}
		layout2_arr=[]
		for header2,field2 in zip(layout_header,layout_field):
			ex_layout_field=field2.split(".")
			is_numeric_field=field2.split("#")
			field_name2=ex_layout_field[0]
			
			if len(is_numeric_field)>1:
				field_type2=is_numeric_field[1]
				field_name2=is_numeric_field[0]
			else:
				field_type2=''  

			if len(ex_layout_field)>1:
				child_name=ex_layout_field[1]
				field_name2=ex_layout_field[0]
			else:
				child_name=''           

			if(layout_check):
				layout_column_fetch=EngageboostGridColumnLayouts.objects.using(company_db).get(module=module,screen_name=screen_name)
				layout_column_header=layout_column_fetch.header_name
				layout_column_field=layout_column_fetch.field_name
				if header2 in layout_column_header:
					status=1
				else:
					status=0
			else:
				status=1        
			layout2={"title":header2,"field":field_name2,"child":child_name,"show":status, "field_type":field_type2}
			layout2_arr.append(layout2)
			##################Applied Layout#####################

		pre_data={}
		final_data=[] 
		pre_data['result']=serializer_product.data 
		pre_data['layout']=layout_arr
		pre_data['applied_layout']=layout2_arr
		final_data.append(pre_data)
		return self.get_paginated_response(final_data)

class VariableProductList(generics.ListAPIView):
# """ List all Products """
	def get_object(self, product_id):
		company_db = loginview.db_active_connection(request)
		try:
			return EngageboostProducts.objects.using(company_db).get(id=product_id)
		except EngageboostProducts.DoesNotExist:
			raise Http404

	def get(self, request, product_id, format=None,partial=True):
		company_db = loginview.db_active_connection(request)
		key = request.GET.get("q")
		
		layout = []

		d2 = {"title": "ID","field": "id","child": "","show": 1,"field_type": ""}
		layout.append(d2)  
		d2 = {"title": "Name","field": "name","child": "","show": 1,"field_type": ""}
		layout.append(d2)
		d2 = {"title": "SKU","field": "sku","child": "","show": 1,"field_type": ""}
		layout.append(d2)

		userObj = EngageboostCossSellProducts.objects.using(company_db).filter(product_id=product_id).exclude(cross_product_id=None).distinct('cross_product_id')
		childIds = EngageboostCossSellProducts.objects.using(company_db).filter(product_id=product_id).exclude(cross_product_id=None).distinct('cross_product_id').values('cross_product_id')
		childs = []
		for item in childIds:
			childs.append(item['cross_product_id'])
		# print("Childs======",childs)    
		# fieldvalueObj = EngageboostMarketplaceFieldValue.objects.using(company_db).filter(product_id=childs)
		fieldvalueObj = EngageboostMarketplaceFieldValue.objects.using(company_db)
		if len(childs)>0:
			fieldvalueObj = fieldvalueObj.filter(product_id__in=childs)
							
		if key!="" and key!=None:
			temp_userObj = userObj.filter(Q(cross_product__id__icontains=key)|Q(cross_product__name__icontains=key)|Q(cross_product__sku__icontains=key))
			if temp_userObj.count()>0:
				userObj=temp_userObj
				####################Fields########################
				if key!="" and key!=None:
					temp_fieldvalueObj = fieldvalueObj.filter(value__icontains=key)
					if temp_fieldvalueObj.count()>0:
						fieldvalueObj = temp_fieldvalueObj

						fields_products = fieldvalueObj.all()

						f_products = []

						for prd in fields_products:
							f_products.append(prd.product_id)    

						userObj = userObj.filter(cross_product_id__in=f_products)
					else: 
						fieldvalueObj = fieldvalueObj   
				####################Fields########################
			else:
				userObj = userObj
				####################Fields########################
				if key!="" and key!=None:
					fieldvalueObj = fieldvalueObj.filter(value__icontains=key)

					fields_products = fieldvalueObj.all()

					f_products = []

					for prd in fields_products:
						f_products.append(prd.product_id)    

					userObj = userObj.filter(cross_product_id__in=f_products)
				####################Fields########################    
		# print("userObj",userObj.count())
			# if fieldvalueObj.count()>0:
				# fields_products = fieldvalueObj.all()

				# f_products = []

				# for prd in fields_products:
				#     f_products.append(prd.product_id)    

				# userObj = userObj.filter(cross_product_id__in=f_products)
		custom_fields = []

		if userObj.count()>0:
			user = userObj.all()
			serializer = CossSellProductsSerializer(user,many=True)
			
		pro_catObj = EngageboostProductCategories.objects.using(company_db).filter(product_id=product_id,is_parent='y')
		# print("pro_catObj",pro_catObj.count())
		if pro_catObj.count()>0:
			
			pro_cat = pro_catObj.first()
			
			category_id = pro_cat.category_id
			# print("category_id===",category_id)
			layoutFieldsobj = EngageboostDefaultModuleLayoutFields.objects.using(company_db).filter(category_id=category_id)
			# print("layoutFieldsobj",layoutFieldsobj.count())
			if layoutFieldsobj.count()>0:
				
				layoutField = layoutFieldsobj.all()
				for val in layoutField:
					
					defaultsfieldsObj = EngageboostDefaultsFields.objects.using(company_db).filter(id=val.field_id,is_variant='Yes')
					# print("defaultsfieldsObj",defaultsfieldsObj.count())
					if defaultsfieldsObj.count()>0:
						
						defaultsfields = defaultsfieldsObj.first()
						field_name = defaultsfields.field_name
						fValue = ""
						field_lable = defaultsfields.name
						fieldvalueObj = fieldvalueObj.filter(field_id=defaultsfields.id)
						if fieldvalueObj.count()>0:
							
							fieldvalue = fieldvalueObj.first()
							fValue = fieldvalue.value

						d1 = {"title": field_lable,"field": field_name,"child": "","show": 1,"field_type": ""}
						# print("Layout====",d1)
						layout.append(d1)
						custom_fields.append({"field_name":field_name,"field_value":fValue})    
							  
			if userObj.count()>0:
				if(serializer):
					for value in serializer.data:
						for cust in custom_fields:
							if value['cross_product']:
								checkField = EngageboostMarketplaceFieldValue.objects.using(company_db).filter(product_id=value['cross_product']['id'])
								if checkField.count()>0:
									value['cross_product'].update({cust['field_name']:cust['field_value']}) 
					data ={
							'status':1,
							'result':serializer.data,
							'layout':layout,
							'message':'Data Found',
						}
				else:
					data ={
							'status':0,
							'api_status':serializer.errors,
							'layout':layout,
							'message':'Data Not Found',
						}
			else:
				data ={
					'status':0,
					'api_status':"",
					'layout':layout,
					'message':'Data Not Found',
				}
		else:
			data ={
				'status':0,
				'api_status':"",
				'layout':layout,
				'message':'Data Not Found',
			}
		return Response(data)
	# Insert new related product 
	def post(self, request, format=None,many=True):
		company_db = loginview.db_active_connection(request)
		has_multy=request.data
		try:
			pro_id = has_multy['product_id']
			existProductId = EngageboostCossSellProducts.objects.filter(product_id=pro_id).values("cross_product_id")
			EngageboostProducts.objects.filter(id__in=existProductId).update(visibility_id = 1)
			if existProductId:
				for tempId in existProductId:
					if tempId['cross_product_id']:
						elastic = common.change_field_value_elastic(int(tempId['cross_product_id']),"EngageboostProducts",{"visibility_id":'Catalog Search'})

			EngageboostCossSellProducts.objects.filter(product_id=pro_id).delete()
			if len(has_multy['post_data'])>0 and 'post_data' in has_multy.keys():
				for data1 in has_multy['post_data']:
					if data1['cross_product_id']!="" and data1['cross_product_id']!=None and 'cross_product_id' in data1.keys():
						d1 = {'product_id':pro_id}
						data1 = dict(data1,**d1)
						serializer = CossSellProductsSerializer(data=data1,partial=True)
						if serializer.is_valid():
							ex_count = EngageboostCossSellProducts.objects.filter(cross_product_id=data1['cross_product_id'],product_id=pro_id).count()

							if ex_count==0:
								EngageboostCossSellProducts.objects.using(company_db).create(**data1)

							data ={
								'status':1,
								'message':'Successfully Saved',
								}
						else:
							data ={
									'status':0,
									'errors':serializer.errors,
									'message':'Data Not Found',
									}
					else:
						data ={
								'status':0,
								'errors':"",
								'message':'Cross product not found',
								}
				newProductId = EngageboostCossSellProducts.objects.filter(product_id=pro_id).values("cross_product_id")
				EngageboostProducts.objects.filter(id__in=newProductId).update(visibility_id = 4)

				if newProductId:
					for tempId in newProductId:
						elastic = common.change_field_value_elastic(int(tempId['cross_product_id']),"EngageboostProducts",{"visibility_id":'Not Visible..'})                
			else:
				data ={
						'status':1,
						'message':'Successfully Saved',
						}
			return Response(data)
		except Exception as error:
			trace_back = sys.exc_info()[2]
			line = trace_back.tb_lineno
			data = {"status":0,"api_status":traceback.format_exc(),"error_line":line,"error_message":str(error),"message": str(error)}                    
			return Response(data)
