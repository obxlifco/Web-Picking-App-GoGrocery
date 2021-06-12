from django.shortcuts import render
from rest_framework.permissions import AllowAny
from rest_framework import generics, permissions, status, views, mixins
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response
from django.http import JsonResponse


from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated

# Import Model And Serializer
from webservices.models import *
from coremodule.coremodule_serializers import *
from django.views.decorators.csrf import csrf_exempt
import json

@permission_classes([])
class CategoryListView(generics.ListAPIView):
    # permission_classes = []
    def get(self, request, format=None):
        website_id = request.META.get('HTTP_WID')
        if website_id:
            pass
        else:
            website_id = 1
           
        rs_category = EngageboostCategoryMasters.objects.filter(isdeleted='n', isblocked='n', website_id=website_id, parent_id=0).all(). order_by('display_order')
        category_data = CategoryMastersSerializer(rs_category, many=True)
        category_data = category_data.data
        if category_data:
            for categorydata in category_data:
                child = {}
                child = GetChildByParent(categorydata['id'], website_id, categorydata['parent_id'])
                if child:
                    categorydata['child']= child
                else:
                    categorydata['child']= []

            data = {
                "status":1,
                "data":category_data
            }
        else:
            data = {
                "status":0,
                "msg":"No data found.",
                "data":[]
            }
        return Response (data)

def GetChildByParent(parent_id, website_id, grand_parent): 
    rs_child = EngageboostCategoryMasters.objects.filter(isdeleted='n', isblocked='n', website_id=website_id, parent_id = parent_id).all(). order_by('display_order')
    child_data = CategoryMastersSerializer(rs_child, many=True)
    child_data = child_data.data
    if child_data:
        for childdata in child_data:
            # childdata['CatId'] = childdata['id']
            # childdata['ParentId'] = childdata['parent_id']
            # childdata['DisplayOrder'] = childdata['display_order']
            # childdata['CatName'] = childdata['name']
            # childdata['CatDescription'] = childdata['description']
            # childdata['CatImage'] = childdata['image']
            # childdata['CatThumbImage'] = childdata['thumb_image']
            # childdata['CatBannerImage'] = childdata['banner_image']
            # childdata['PagTitle'] = childdata['page_title']
            # childdata['MetaDescription'] = childdata['meta_description']
            # childdata['MetaKeywords'] = childdata['meta_keywords']
            # childdata['CatSlug'] = childdata['slug']
            childdata['grand_parent_id'] = grand_parent
            child = {}
            child = GetChildByParent(childdata['id'], website_id, childdata['parent_id'])
            if child:
                childdata['child'] = child
            else:
                childdata['child'] = []
        
    return child_data

class GetCategoryListById(generics.ListAPIView):

    def get(self, request, pk, format=None):
        website_id = request.META.get('HTTP_WID')
        if website_id:
            pass
        else:
            website_id = 1
        parent_id = pk
        rs_category = EngageboostCategoryMasters.objects.filter(isdeleted='n', isblocked='n', website_id=website_id, id = pk).all(). order_by('display_order')
        category_data = CategoryMastersSerializer(rs_category, many=True)
        category_data = category_data.data
        if category_data:
            for categorydata in category_data:
                # categorydata['CatId'] = categorydata['id']
                # categorydata['ParentId'] = categorydata['parent_id']
                # categorydata['DisplayOrder'] = categorydata['display_order']
                # categorydata['CatName'] = categorydata['name']
                # categorydata['CatDescription'] = categorydata['description']
                # categorydata['CatImage'] = categorydata['image']
                # categorydata['CatThumbImage'] = categorydata['thumb_image']
                # categorydata['CatBannerImage'] = categorydata['banner_image']
                # categorydata['PagTitle'] = categorydata['page_title']
                # categorydata['MetaDescription'] = categorydata['meta_description']
                # categorydata['MetaKeywords'] = categorydata['meta_keywords']
                # categorydata['CatSlug'] = categorydata['slug']

                child = {}
                child = GetChildByParent(categorydata['id'], website_id, categorydata['parent_id'])
                if child:
                    categorydata['child']= child
                else:
                    childdata['child'] = []

            data = {
                "status":1,
                "data":category_data
            }
        else:
            data = {
                "status":0,
                "msg":"No data found.",
                "data":[]
            }
        return Response (data)

class GetSubCategoryByParent(generics.ListAPIView):
    def get(self, request, pk, format=None):
        website_id = request.META.get('HTTP_WID')
        if website_id:
            pass
        else:
            website_id = 1
        parent_id = pk
        rs_category = EngageboostCategoryMasters.objects.filter(isdeleted='n', isblocked='n', website_id=website_id, parent_id = parent_id).all(). order_by('display_order')
        category_data = CategoryMastersSerializer(rs_category, many=True)
        category_data = category_data.data
        if category_data:
            for categorydata in category_data:
                # categorydata['CatId'] = categorydata['id']
                # categorydata['ParentId'] = categorydata['parent_id']
                # categorydata['DisplayOrder'] = categorydata['display_order']
                # categorydata['CatName'] = categorydata['name']
                # categorydata['CatDescription'] = categorydata['description']
                # categorydata['CatImage'] = categorydata['image']
                # categorydata['CatThumbImage'] = categorydata['thumb_image']
                # categorydata['CatBannerImage'] = categorydata['banner_image']
                # categorydata['PagTitle'] = categorydata['page_title']
                # categorydata['MetaDescription'] = categorydata['meta_description']
                # categorydata['MetaKeywords'] = categorydata['meta_keywords']
                # categorydata['CatSlug'] = categorydata['slug']

                rs_parent = EngageboostCategoryMasters.objects.filter(isdeleted='n', isblocked='n', website_id=website_id, id = parent_id).first()
                # dd = CategoryMastersSerializer(rs_parent)
                # print(json.dumps(dd.data, indent=4, sort_keys=True))
                if rs_parent:
                    categorydata['grand_parent_id'] = rs_parent.parent_id
                else:
                    categorydata['grand_parent_id'] = 0

                child = {}
                child = GetChildByParent(categorydata['id'], website_id, categorydata['parent_id'])
                if child:
                    categorydata['child']= child
                else:
                    categorydata['child'] = []

            data = {
                "status":1,
                "data":category_data
            }
        else:
            data = {
                "status":0,
                "msg":"No data found.",
                "data":[]
            }
        return Response (data)
def rename(self,key,new_key):
    ind = self._keys.index(key)  # get the index of old key, O(N) operation
    self._keys[ind] = new_key    # replace old key with new key in self._keys
    self[new_key] = self[key]    # add the new key, this is added at the end of self._keys
    self._keys.pop(-1)           # pop the last item in self._keys

class ParentCategoryListView(generics.ListAPIView):

    def get(self, request, format=None):
        website_id = request.META.get('HTTP_WID')
        if website_id:
            pass
        else:
            website_id = 1
           
        rs_category = EngageboostCategoryMasters.objects.filter(isdeleted='n', isblocked='n', website_id=website_id, parent_id=0).all(). order_by('display_order').iterator()
        category_data = CategoryMastersSerializer(rs_category, many=True)
        category_data = category_data.data
        if category_data:
            
            data = {
                "status":1,
                "data":category_data
            }
        else:
            data = {
                "status":0,
                "msg":"No data found.",
                "data":[]
            }
        return Response (data)



def GetChildByParentSelected(parent_id, website_id, grand_parent): 
    rs_child = EngageboostCategoryMasters.objects.filter(isdeleted='n', isblocked='n', website_id=website_id, parent_id = parent_id).all(). order_by('display_order')
    child_data = CategoryMastersNameSerializer(rs_child, many=True)
    child_data = child_data.data
    if child_data:
        for childdata in child_data:
            childdata['grand_parent_id'] = grand_parent
            child = {}
            child = GetChildByParentSelected(childdata['id'], website_id, childdata['parent_id'])
            if child:
                childdata['child'] = child
            else:
                childdata['child'] = []
        
    return child_data  

@csrf_exempt
def categorylisting(request,wid):
    #website_id = request.META.get('HTTP_WID')
    website_id=wid
    if website_id:
        pass
    else:
        website_id = 1
    data = {}
    list_category = EngageboostCategoryMasters.objects.filter(isdeleted='n', isblocked='n', website_id=website_id, parent_id=0).all(). order_by('display_order')
    categorylist_data = CategoryMastersNameSerializer(list_category, many=True)
    categorylist_data = categorylist_data.data
    if categorylist_data:
        for categorylistdata in categorylist_data:
            child = {}
            child = GetChildByParentSelected(categorylistdata['id'], website_id, categorylistdata['parent_id'])
            if child:
                categorylistdata['child']= child
            else:
                categorylistdata['child'] = []

        data = {
            "status":1,
            "data":categorylist_data
        }
    else:
        data = {
            "status":0,
            "msg":"No data found.",
            "data":[]
        }

    return JsonResponse (data)

      
            
