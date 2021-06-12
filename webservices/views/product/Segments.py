from webservices.models import EngageboostEmktSegments,EngageboostEmktSegmentContactlists,EngageboostEmktContacts,EngageboostEmktContactlists
from django.http import Http404
from webservices.serializers import SegmentsSerializer,SegmentsContactlistsSerializer,ContactsSerializer
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
from django.http import HttpResponse
import json
from webservices.views import loginview

class Segments(generics.ListAPIView):
# """ List all users, or create a new user """
    def post(self, request, format=None):
        company_db = loginview.db_active_connection(request)
        d1={'created':datetime.now().date(),'modified':datetime.now().date()}
        d2=request.data
        serializer_data=dict(d2,**d1)
        serializer = SegmentsSerializer(data=serializer_data,partial=True)
        if serializer.is_valid():
            serializer.save()
            obj = EngageboostEmktSegments.objects.using(company_db).latest('id')
            last_id = obj.id
            d4=request.data
            rows=d4['contact_id']
            menu_group=rows.split(",")
            # menu_group=[int(x) for x in menu_group]
            for data in menu_group:
                # print(data)
                con=EngageboostEmktContacts.objects.using(company_db).all().filter(contact_list_id=data)
                for c in con:
                    for data in menu_group:
                        EngageboostEmktSegmentContactlists.objects.using(company_db).create(contact_id=c.id,segment_id=last_id,created=datetime.now().date(),modified=datetime.now().date(),contactlist_id=data,segment_contactlistname=d4['segment_name'])
                        data ={
                        'status':1,
                        'api_status':'',
                        'message':'Successfully Inserted',
                        }
                    return Response(data)

class SegmentsList(generics.ListAPIView):
# """ List all users, or create a new user """
    def get_object(self, pk,request):
        company_db = loginview.db_active_connection(request)
        try:
            return EngageboostEmktSegments.objects.using(company_db).get(pk=pk)
        except EngageboostEmktSegments.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None,partial=True):
        company_db = loginview.db_active_connection(request)
        user = self.get_object(pk,request)
        serializer = SegmentsSerializer(user)
        Conditions = EngageboostEmktSegmentContactlists.objects.using(company_db).all().filter(isdeleted='n',segment_id=pk)
        serializer_data = SegmentsContactlistsSerializer(Conditions,many=True)
        arr=[]
        for c in Conditions:
            ids=c.contactlist_id
            # arr1=[]
            Conditions_list1 = EngageboostEmktContactlists.objects.using(company_db).all().filter(isdeleted='n',id=ids)   
            for c1 in Conditions_list1:
                # print(c1.name)
                arr.append(c1.id)                   
        Conditions_list = EngageboostEmktContactlists.objects.using(company_db).all().filter(isdeleted='n')
        arr2=[]
        for c2 in Conditions_list:
            # print(c2.id)
            if c2.id in arr:
                # print(c2.name)
                d2={"id":c2.id,"name":c2.name,"status":1}
            else:
                d2={"id":c2.id,"name":c2.name,"status":0}
            arr2.append(d2)
        return HttpResponse(json.dumps({"Segments": serializer.data,"Contact":arr2}), content_type='application/json')
        
    def put(self, request, pk, format=None,partial=True):
        company_db = loginview.db_active_connection(request)
        seg = self.get_object(pk,request)
        d1={'modified':datetime.now().date()}
        d2=request.data
        serializer_data=dict(d2,**d1)
        serializer = SegmentsSerializer(seg,data=serializer_data,partial=True)
        if serializer.is_valid():
            serializer.save()
            obj = EngageboostEmktSegments.objects.using(company_db).latest('id')
            last_id = obj.id
            d4=request.data
            rows=d4['contact_id']
            menu_group=rows.split(",")
            # menu_group=[int(x) for x in menu_group]
            EngageboostEmktSegmentContactlists.objects.using(company_db).filter(segment_id=pk).delete()
            for data in menu_group:
                con=EngageboostEmktContacts.objects.using(company_db).all().filter(contact_list_id=data)
                for c in con:
                    for data in menu_group:
                        EngageboostEmktSegmentContactlists.objects.using(company_db).create(contact_id=c.id,segment_id=last_id,created=datetime.now().date(),modified=datetime.now().date(),contactlist_id=data,segment_contactlistname=d4['segment_name'])
                        data ={
                        'status':1,
                        'api_status':'',
                        'message':'Successfully Updated',
                        }
                    return Response(data)