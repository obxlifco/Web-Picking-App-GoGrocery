import requests
from django.http import HttpResponse
from django.apps import apps
from rest_framework import generics,viewsets
from rest_framework.response import Response
import json
from webservices.models import *
from webservices.views import loginview
from webservices.views.settings.GlobalList import GlobalList
from webservices.serializers import *
from django.shortcuts import get_object_or_404
from decimal import *
from elasticsearch import Elasticsearch
from elasticsearch import helpers
from webservices.views.common import common
es = Elasticsearch([{'host': 'navsoft.co.in', 'port': 9200}])

class ESMenuViewSet(generics.ListAPIView):
# """ List all Menu for Elastic Search """

	def post(self, request, format=None):
		company_db = loginview.db_active_connection(request)
		key=request.data.get('key')
		module=request.data.get('module')
		offset=request.data.get('offset')
		limit=request.data.get('limit')
		userid = request.data.get('userid')
		if limit==None or limit=="":
			limit=5
		if offset==None or offset=="":
			offset=0	
		if module==None or module=="":
			# res = requests.get('http://navsoft.co.in:9200/searchdata/'+module+'/_search/?q=*'+key+'*&size='+limit+'&from='+offset)
			res = requests.get('http://navsoft.co.in:9200/searchdata/'+module+'/_search/?q=*'+key+'*&size='+limit+'&from='+offset) 
		else:
			res = requests.get('http://navsoft.co.in:9200/searchdata/_search/?q=*'+key+'*&size='+limit+'&from='+offset) 
		return HttpResponse(res.content)	

class ESMenuActionViewSet(generics.ListAPIView):
# """ Add/Update Menu for Elastic Search """

	def post(self, request, format=None):
		company_db = loginview.db_active_connection(request)
		child_menu = EngageboostMenuMasters.objects.using(company_db).all().filter(isdeleted=0,isblocked=0).exclude(parent_id =0)
		for cm in child_menu:
			cm_id=str(cm.id)
			parent_id=cm.parent_id
			parent_menu = EngageboostMenuMasters.objects.using(company_db).get(id=parent_id)
			data={"name":cm.name,"link":cm.link,"parent_id":cm.parent_id,"parent_name":parent_menu.name,"parent_css":parent_menu.css_class}
			resp = requests.post("http://navsoft.co.in:9200/searchdata/menu/"+cm_id, data=json.dumps(data),  # serialize the dictionary from above into json
				headers={
						   "Content-Type":"application/json",
						   "Accept": "application/json"
						})
			print(resp.status_code)
			print(resp.content)
		return HttpResponse(resp.content)

	def put(self, request, format=None):
		company_db = loginview.db_active_connection(request)
		child_menu = EngageboostMenuMasters.objects.using(company_db).all().filter(isdeleted=0,isblocked=0).exclude(parent_id =0)
		for cm in child_menu:
			cm_id=str(cm.id)
			parent_id=cm.parent_id
			parent_menu = EngageboostMenuMasters.objects.using(company_db).get(id=parent_id)
			data={"name":cm.name,"link":cm.link,"parent_id":cm.parent_id,"parent_name":parent_menu.name,"parent_css":parent_menu.css_class}
			resp = requests.put("http://navsoft.co.in:9200/searchdata/menu/"+cm_id, data=json.dumps(data),  # serialize the dictionary from above into json
				headers={
						   "Content-Type":"application/json",
						   "Accept": "application/json"
						})
			print(resp.status_code)
			print(resp.content)
		return HttpResponse(resp.content)	

	def delete(self, request, format=None):
		resp = requests.delete("http://navsoft.co.in:9200/searchdata/product", data="",  # serialize the dictionary from above into json
			headers={
					   "Content-Type":"application/json",
					   "Accept": "application/json"
					})
		print(resp.status_code)
		print(resp.content)
		return HttpResponse(resp.content)
				

class ESDataActionViewSet(generics.ListAPIView):
# """ Add/Update Data for Elastic Search """
	def get(self, request, format=None):
		company_db = loginview.db_active_connection(request)
		key=request.GET.get('key')
		index=request.GET.get('index')
		if index is None or index==None or index=="":
			index="searchdata"
		module=request.GET.get('module')
		offset=request.GET.get('offset')
		limit=request.data.get('limit')
		if limit==None or limit=="":
			limit=5
		if offset==None or offset=="":
			offset=0	
		res = requests.get('http://navsoft.co.in:9200/'+index+'/'+module+'/_search/?q=*'+key+'*&size='+limit+'&from='+offset) 
		return HttpResponse(res.content)

	def get_company_name(self, website_id):
		website = EngageboostCompanyWebsites.objects.get(id=website_id)
		website_data = CompanyWebsiteSerializer(website,partial=True)
		company_name = ""
		if website_data.data['company_name']!="" and website_data.data['company_name']!=None:
			company_name = website_data.data['company_name']
		return company_name

	def delete_index(self, website_id, table, company):
		if table=="EngageboostProducts":
			module_name = "product"

		elif table=="EngageboostCategoryMasters":
			module_name = "category"

		elif table=="EngageboostCustomers":
			module_name = "customer"

		elif table=="EngageboostOrdermaster":
			module_name = "order"
		
		module_name = module_name+"_"+company+"_"+str(website_id)	
		dlt = es.indices.delete(index=module_name, ignore=[400, 404])
		
		if 'acknowledged' in dlt.keys() and dlt['acknowledged']==True:
			msg = module_name+" deleted"
			status = 1
		else:
			msg = module_name+" not exists"
			status = 0
		data = {
				"status":status,
				"msg":msg
			}
		return data		

	def get_object(self, model, serializer):
		
		datas = {}
		company_name=""
		
		if model=="EngageboostProducts":
			cm_id=str(serializer['id'])
			
			link ='products/edit/'+cm_id
			tab_name ='Edit Product'
			tab_id ='productsedit'
			
			data ={
					"link":link,
					"tab_name":tab_name,
					"tab_id":tab_id
				}	
			data = dict(serializer,**data)	
			
			module_name = "product"

			# datas={"data":data,"id":cm_id,"module_name":module_name}

		elif model=="EngageboostCategoryMasters":
			cm_id=str(serializer['id'])
			
			link ='category/edit/'+cm_id
			tab_name ='Edit Category'
			tab_id ='categoryedit'
			
			data ={
					"link":link,
					"tab_name":tab_name,
					"tab_id":tab_id
				}	
			data = dict(serializer,**data)	
			
			module_name = "category"

			# datas={"data":data,"id":cm_id,"module_name":module_name}

		elif model=="EngageboostCustomers":
			cm_id=str(serializer['id'])
			
			link ='customers/edit/'+cm_id
			tab_name ='Edit Customer'
			tab_id ='customersedit'
			
			data ={
					"link":link,
					"tab_name":tab_name,
					"tab_id":tab_id
				}	
			data = dict(serializer,**data)	
			
			module_name = "customer"

			# datas={"data":data,"id":cm_id,"module_name":module_name}

		elif model=="EngageboostOrdermaster":
			cm_id=str(serializer['id'])
			
			link ='orders/edit/'+cm_id
			tab_name ='Edit Order'
			tab_id ='ordersedit'
			
			data ={
					"link":link,
					"tab_name":tab_name,
					"tab_id":tab_id
				}	
			data = dict(serializer,**data)	
			
			module_name = "order"

			# datas={"data":data,"id":cm_id,"module_name":module_name}

		elif model=="EngageboostDiscountMasters":
			cm_id=str(serializer['id'])
			
			link ='promotions/edit/'+cm_id
			tab_name ='Edit Promotion'
			tab_id ='promotionsedit'
			
			data ={
					"link":link,
					"tab_name":tab_name,
					"tab_id":tab_id
				}	
			data = dict(serializer,**data)	
			
			module_name = "promotion"

			# datas={"data":data,"id":cm_id,"module_name":module_name}	
		data = common.setUpLangDataToSerializer(data)
		# print(data)
		datas={"data":data,"id":cm_id,"module_name":module_name}

		return datas	

	def post(self, request, format=None):
		d2 = request.data
		show = d2["show"]
		table_name = d2["model"]
		indexes = ["searchdata"]

		model=apps.get_model('webservices',table_name)
		company_db = loginview.db_active_connection(request)
		serializer_class = common.get_serializer_class_elastic(table_name)
		
		datas = []
		docs = []
		
		websitesObj = EngageboostCompanyWebsites.objects.filter(isblocked='n',isdeleted='n')
		if websitesObj.count()>0:
			websites = websitesObj.all()
			
			for website in websites:
				# company_name = website.company_name

				# company_name=company_name.lower()
				# company_name=company_name.replace(" ","-")
				company_name = "lifco"
				website_id = website.id
				prod_obj = model.objects.filter(website_id=website.id)		
		
				if prod_obj.count()>0:
								
					# products = prod_obj.all()
					products = prod_obj[0:1000]
					# print(products.query)
					products_data = serializer_class(products,many=True)
					
					for serializer in products_data.data:
						values = self.get_object(table_name,serializer)

						cm_id=values["id"]
						data =values["data"]
						module_name =values["module_name"]
						module_name = company_name+"_"+module_name+"_"+str(website_id)
						# module_name = common.get_index_name_elastic(serializer['id'],table_name)
						# module_name = "boost_test"
						# serializer['id'] = 555
						common.check_mapping_elastic(module_name,table_name)

						header = {
							"_index": module_name,
							"_type": "data",
							"_id": cm_id,
							"_source": data
						}
						docs.append(header)
					
					if show=="1":
						datas.append(docs)
					else:
						# self.delete_index(website_id, table_name, company_name)
						obj = helpers.bulk(es,docs)
						datas.append("Success")
	
				
		return Response(datas)		

	def delete(self, request, format=None):
		d2 = request.data
		table_name = d2["model"]
		indexes = ["searchdata"]

		datas = []
		docs = []
		
		companiesObj = EngageboostCompanies.objects

		if companiesObj.count()>0:
			companies = companiesObj.all()
			
			for company in companies:
				
				websitesObj = EngageboostCompanyWebsites.objects.filter(engageboost_company_id=company.id)
				if websitesObj.count()>0:
					websites = websitesObj.all()
					
					for website in websites:
						website_id = website.id
						company_name = website.company_name

						company_name=company_name.lower()
						company_name=company_name.replace(" ","-")

						indices = self.delete_index(website_id, table_name, company_name)
						datas.append(indices['msg'])
		else:
			datas.append("Failed")	
				
		return Response(datas)


class ModifySku(generics.ListAPIView):
	def post(self, request, format=None):
		fetchGlobalSettings=EngageboostGlobalSettings.objects.get(website_id=1)
		prefixs = ""
		suffixs = ""
		if fetchGlobalSettings.sku_prefix!="" and fetchGlobalSettings.sku_prefix!=None:
			prefixs = fetchGlobalSettings.sku_prefix
		if fetchGlobalSettings.sku_suffix!="" and fetchGlobalSettings.sku_suffix!=None:
			suffixs = fetchGlobalSettings.sku_suffix    
		data = []	
		skus=EngageboostProducts.objects.exclude(sku__startswith=prefixs,sku__endswith=suffixs).all()
		for item in skus:
			sku=prefixs+item.sku+suffixs
			EngageboostProducts.objects.filter(id=item.id).update(sku=sku)
			data.append(item.sku)
		return Response(data)

