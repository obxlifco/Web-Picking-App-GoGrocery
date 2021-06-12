from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt, ensure_csrf_cookie
from rest_framework import generics, permissions, status, views, mixins
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response
from rest_framework import status

from django.http import JsonResponse
from django.db.models import F, Func, FloatField
from django.db.models.functions import Cast

from webservices.models import *
from frontapp.frontapp_serializers import *

import json
import base64
import sys,os
import traceback
import datetime
from django.db.models import Q
from django.contrib.auth.hashers import make_password,check_password
import random
from webservices.views.emailcomponent import emailcomponent
from frontapp.views.sitecommon import common_functions

class LoginView(APIView): 
    permission_classes = []
    def post(self, request, format=None):
        requestdata = JSONParser().parse(request)
        user_mail  = requestdata['user_mail'].strip()
        user_passw = requestdata['user_password'].strip()
        device_id = request.META.get('HTTP_DEVICEID')
        now_utc = datetime.datetime.now(datetime.timezone.utc).astimezone()
        str_status = ""
        try:
            if user_mail== '':
                raise Exception("Username is required") 
            if user_passw== '':
                raise Exception("Password is required") 

            usrExist=EngageboostUsers.objects.filter(Q(email__iexact=user_mail) | Q(username=user_mail) | Q(phone=user_mail)).filter(isdeleted='n').count()
            custExist = EngageboostCustomers.objects.filter(Q(email__iexact=user_mail) | Q(phone=user_mail)).filter(isdeleted='n').count()
            
            if usrExist> 0 and custExist>0:
                usrBlock=EngageboostUsers.objects.filter(Q(email__iexact=user_mail) | Q(username=user_mail) | Q(phone=user_mail)).filter(isdeleted='n',isblocked='y').count()
                custBlock = EngageboostCustomers.objects.filter(Q(email__iexact=user_mail) | Q(phone=user_mail)).filter(isdeleted='n',isblocked='y').count()
                if usrBlock>0 or custBlock>0:
                    str_status = status.HTTP_204_NO_CONTENT
                    data = {
                        'status':str_status,
                        'message': 'Your account has been blocked.',
                        'data':{}
                        }

                else:
                    User=EngageboostUsers.objects.filter(Q(email__iexact=user_mail) | Q(username=user_mail) | Q(phone=user_mail)).filter(isblocked='n',isdeleted='n').latest('id')
                    User_data = EngageboostUsersSerializers(User).data
                    token=Token.objects.get_or_create(user=User)
                    auth = Token.objects.filter(user_id=User.id).latest('user_id')
                    token = auth.key
                    User_data.update({'token':token}) 
                    
                    if User:    
                        user_type = User.user_type
                        password_check = User.check_password(user_passw)
                        isblocked = User.isblocked
                        isdeleted = User.isdeleted 
                    if password_check==True and user_type == 'frontend' and isdeleted =='n' and isblocked == 'n':
                        str_status = status.HTTP_200_OK
                        if device_id is not None and token is not None:
                            rs_up = EngageboostTemporaryShoppingCarts.objects.filter(device_id=device_id, customer_id__isnull=True).update(customer_id=User.id)
                        
                        # Update Last Login
                        rs_user = EngageboostUsers.objects.filter(id = User.id).update(last_login=now_utc)

                        data = {
                            'status':str_status,
                            'message': 'Username / password  match.',
                            'data':User_data
                            }
                    
                    else:
                        str_status = status.HTTP_204_NO_CONTENT
                        data = {
                            'status':str_status,
                            'message': 'Password mismatch.',
                            'data':{}
                            }
            else:
                str_status = status.HTTP_204_NO_CONTENT
                data = {
                        'status':str_status,
                        'message': 'Username mismatch.',
                        'data':{}
                        }

        except Exception as error:
            trace_back = sys.exc_info()[2]
            line = trace_back.tb_lineno
            str_status = status.HTTP_417_EXPECTATION_FAILED
            data = {"status": str_status, "api_status": traceback.format_exc(), "error_line": line, "error_message": str(error),"message": str(error)}
        return Response (data)

class SignupView(APIView): 
    permission_classes = []
    def post(self, request, format=None):
        requestdata     = JSONParser().parse(request)
        user_email      = requestdata['user_email'].strip()
        user_password   = requestdata['user_password']
        hash_password   = make_password(user_password, None, 'md5')
        name            = requestdata['name']
        address = ""
        if "address" in requestdata:
            address         = requestdata['address']
        phone           = requestdata['phone']
        device_id       = request.META.get('HTTP_DEVICEID')
        website_id = request.META.get('HTTP_WID')
        now_utc = datetime.datetime.now(datetime.timezone.utc).astimezone()
       
        first_name, *last_name = name.split()
        space_index = user_email.split("@")[0]
        number = '{:03d}'.format(random.randrange(1, 999))
        username = (space_index + number)
        if website_id is None:
            website_id = 1
        if website_id<=0:
            website_id = 1
        
        try:
            
            if user_email=='':
                raise Exception("email is required") 
            if user_password=='':
                raise Exception("password is required") 
            if name=='':
                raise Exception("name is required")  
            # if address=='':
            #     raise Exception("address is required")
            if phone=='':
                raise Exception("phone is required")
            # data["first_name"]= new[0]
            # data["last_name"]= new[1] 
  
            # cnt=EngageboostUsers.objects.filter(Q(email__iexact=user_email) | Q(phone=phone)).filter(isblocked='n',isdeleted='n').count()
            # cstTabCheck = EngageboostCustomers.objects.filter(Q(email__iexact=user_email) | Q(phone=phone)).filter(isdeleted='n',isblocked ='n').count()

            cstTabCheck = EngageboostCustomers.objects.filter(Q(email__iexact=user_email) | Q(phone=phone)).filter(isdeleted='n').count()
            custBlock= EngageboostCustomers.objects.filter(Q(email__iexact=user_email) | Q(phone=phone)).filter(isdeleted='n',isblocked ='y').count()
            #print(cstTabCheck)
            if cstTabCheck>0:
                raise Exception("Email / Mobile already exist")
            elif (cstTabCheck==0 and custBlock>0):
                
                raise Exception("Your account has been blocked.")
            else:
                User=EngageboostUsers.objects.create(
                    email = user_email, 
                    password = hash_password,
                    username = username,
                    first_name = first_name,
                    last_name=" ".join(last_name),
                    phone = phone,
                    date_joined = now_utc,
                    company_id = 1,
                    created_date = now_utc,
                    modified_date = now_utc,
                    user_type='frontend',
                    website_id=website_id
                )
                User.save()
                user_data = EngageboostUsersSerializers(User).data
                token=Token.objects.get_or_create(user=User)
                auth = Token.objects.filter(user_id=User.id).first()
                token = auth.key
                user_data.update({'token':token}) 
            
                customer=EngageboostCustomers.objects.create(
                    auth_user_id = User.id,
                    email = user_email, 
                    password = hash_password,
                    first_name = first_name,
                    last_name=" ".join(last_name),
                    address = address,
                    phone = phone,
                    created = now_utc,
                    modified = now_utc,
                    website_id=website_id
                    
                )
                customer.save()
                buffer_data = common_functions.getAutoResponder("","","","","",24)
                if buffer_data and buffer_data["content"]:
                    autoResponderData  = buffer_data["content"]
                if autoResponderData["email_type"] == 'H':
                    emailContent = autoResponderData["email_content"]
                else:
                    emailContent = autoResponderData["email_content_text"]
                emailContent = str(emailContent)
                emailContent = emailContent.replace('{@first_name}',first_name)
                emailContent = emailContent.replace('{@email}',user_email)
                emailContent = emailContent.replace('{@phone}',phone)
                if User:
                    emailcomponent.OrderMail(user_email,autoResponderData["email_from"],autoResponderData["subject"],emailContent)
                    str_status = status.HTTP_200_OK
                    if device_id is not None and token is not None:
                        rs_up = EngageboostTemporaryShoppingCarts.objects.filter(device_id=device_id, customer_id__isnull=True).update(customer_id=User.id)

                    data = {
                        'status':str_status,
                        'message': 'you have successfully signed up.',
                        'data':user_data
                        }
               
        except Exception as error:
            trace_back = sys.exc_info()[2]
            line = trace_back.tb_lineno
            str_status = status.HTTP_417_EXPECTATION_FAILED
            data = {"status": str_status, "api_status": traceback.format_exc(), "error_line": line, "error_message": str(error),"message": str(error)}
        return Response (data,str_status)

#-----Test-----#
class LoginViewTest(APIView):
    permission_classes = []

    def post(self, request, format=None):
        requestdata = JSONParser().parse(request)
        user_mail = requestdata['user_mail'].strip()
        user_passw = requestdata['user_password'].strip()
        device_id = request.META.get('HTTP_DEVICEID')
        str_status = ""
        now_utc = datetime.datetime.now(datetime.timezone.utc).astimezone()
        try:
            if user_mail == '':
                raise Exception("Username is required")
            if user_passw == '':
                raise Exception("Password is required")

            usrExist = EngageboostUsers.objects.filter(
                Q(email__iexact=user_mail) | Q(username=user_mail) | Q(phone=user_mail)).filter(isdeleted='n').count()
            custExist = EngageboostCustomers.objects.filter(Q(email__iexact=user_mail) | Q(phone=user_mail)).filter(
                isdeleted='n').count()

            if usrExist > 0 and custExist > 0:
                usrBlock = EngageboostUsers.objects.filter(
                    Q(email__iexact=user_mail) | Q(username=user_mail) | Q(phone=user_mail)).filter(isdeleted='n',
                                                                                                    isblocked='y').count()
                custBlock = EngageboostCustomers.objects.filter(Q(email__iexact=user_mail) | Q(phone=user_mail)).filter(
                    isdeleted='n', isblocked='y').count()

                # usrVerified = EngageboostUsers.objects.filter(
                #     Q(email__iexact=user_mail) | Q(username=user_mail) | Q(phone=user_mail)).filter(isdeleted='n',
                #                                                                                     is_verified='y').count()
                if usrBlock > 0 or custBlock > 0:
                    str_status = status.HTTP_204_NO_CONTENT
                    data = {
                        'status': str_status,
                        'message': 'Your account has been blocked.',
                        'data': {}
                    }

                # elif usrVerified == 0:
                #     str_status = status.HTTP_204_NO_CONTENT
                #     data = {
                #         'status': str_status,
                #         'message': 'Your account phone number is not verified.',
                #         'data': {}
                #     }

                else:
                    User = EngageboostUsers.objects.filter(
                        Q(email__iexact=user_mail) | Q(username=user_mail) | Q(phone=user_mail)).filter(isblocked='n',
                                                                                                        isdeleted='n').latest(
                        'id')
                    User_data = EngageboostUsersSerializers(User).data
                    token = Token.objects.get_or_create(user=User)
                    auth = Token.objects.filter(user_id=User.id).latest('user_id')
                    token = auth.key
                    User_data.update({'token': token})

                    if User:
                        user_type = User.user_type
                        password_check = User.check_password(user_passw)
                        isblocked = User.isblocked
                        isdeleted = User.isdeleted
                    if password_check == True and user_type == 'frontend' and isdeleted == 'n' and isblocked == 'n':
                        str_status = status.HTTP_200_OK
                        if device_id is not None and token is not None:
                            rs_up = EngageboostTemporaryShoppingCarts.objects.filter(device_id=device_id,
                                                                                     customer_id__isnull=True).update(
                                customer_id=User.id)

                        # Update Last Login
                        rs_user = EngageboostUsers.objects.filter(id=User.id).update(last_login=now_utc)

                        data = {
                            'status': str_status,
                            'message': 'Username / password  match.',
                            'data': User_data
                        }

                    else:
                        str_status = status.HTTP_204_NO_CONTENT
                        data = {
                            'status': str_status,
                            'message': 'Password mismatch.',
                            'data': {}
                        }
            else:
                str_status = status.HTTP_204_NO_CONTENT
                data = {
                    'status': str_status,
                    'message': 'Username mismatch.',
                    'data': {}
                }

        except Exception as error:
            trace_back = sys.exc_info()[2]
            line = trace_back.tb_lineno
            str_status = status.HTTP_417_EXPECTATION_FAILED
            data = {"status": str_status, "api_status": traceback.format_exc(), "error_line": line,
                    "error_message": str(error), "message": str(error)}
        return Response(data)


class SignupViewTest(APIView):
    permission_classes = []

    def post(self, request, format=None):
        requestdata = JSONParser().parse(request)
        user_email = requestdata['user_email'].strip()
        user_password = requestdata['user_password']
        hash_password = make_password(user_password, None, 'md5')

        if "first_name" in requestdata:
            first_name = requestdata['first_name']
        if "last_name" in requestdata:
            last_name = requestdata['last_name']

        # name            = requestdata['name']

        address = ""
        if "address" in requestdata:
            address = requestdata['address']

        if "name" in requestdata:
            name = requestdata['name']

            first_name, *last_name = name.split()

        # phone           = requestdata['phone']
        device_id = request.META.get('HTTP_DEVICEID')
        website_id = request.META.get('HTTP_WID')
        now_utc = datetime.datetime.now(datetime.timezone.utc).astimezone()

        # first_name, *last_name = name.split()
        space_index = user_email.split("@")[0]
        number = '{:03d}'.format(random.randrange(1, 999))
        username = (space_index + number)
        if website_id is None:
            website_id = 1
        if website_id <= 0:
            website_id = 1

        try:

            if user_email == '':
                raise Exception("email is required")
            if user_password == '':
                raise Exception("password is required")
            if "name" in requestdata:
                if name == '':
                    raise Exception("name is required")

            if "first_name" in requestdata:
                if first_name == '':
                    raise Exception("first name is required")

            if "last_name" in requestdata:
                if last_name == '':
                    raise Exception("last name is required")
            # if address=='':
            #     raise Exception("address is required")
            # if phone=='':
            #     raise Exception("phone is required")
            # data["first_name"]= new[0]
            # data["last_name"]= new[1]

            # cnt=EngageboostUsers.objects.filter(Q(email__iexact=user_email) | Q(phone=phone)).filter(isblocked='n',isdeleted='n').count()
            # cstTabCheck = EngageboostCustomers.objects.filter(Q(email__iexact=user_email) | Q(phone=phone)).filter(isdeleted='n',isblocked ='n').count()
            cstTabCheck = EngageboostCustomers.objects.filter(email__iexact=user_email).filter(isdeleted='n').count()
            # cstTabCheck = EngageboostCustomers.objects.filter(Q(email__iexact=user_email) | Q(phone=phone)).filter(isdeleted='n').count()
            custBlock = EngageboostCustomers.objects.filter(email__iexact=user_email).filter(isdeleted='n',
                                                                                             isblocked='y').count()
            # custBlock= EngageboostCustomers.objects.filter(Q(email__iexact=user_email) | Q(phone=phone)).filter(isdeleted='n',isblocked ='y').count()
            # print(cstTabCheck)
            if cstTabCheck > 0:
                raise Exception("Email already exist")
                # raise Exception("Email / Mobile already exist")
            elif (cstTabCheck == 0 and custBlock > 0):

                raise Exception("Your account has been blocked.")
            else:

                if "name" in requestdata:
                    last_name = " ".join(last_name)

                User = EngageboostUsers.objects.create(
                    email=user_email,
                    password=hash_password,
                    username=username,
                    first_name=first_name,
                    last_name=last_name,
                    # last_name=" ".join(last_name),
                    # phone = phone,
                    date_joined=now_utc,
                    company_id=1,
                    created_date=now_utc,
                    modified_date=now_utc,
                    user_type='frontend',
                    website_id=website_id
                )
                User.save()
                user_data = EngageboostUsersSerializers(User).data

                token = Token.objects.get_or_create(user=User)
                auth = Token.objects.filter(user_id=User.id).first()
                token = auth.key

                user_data.update({'token': token})

                customer = EngageboostCustomers.objects.create(
                    auth_user_id=User.id,
                    email=user_email,
                    password=hash_password,
                    first_name=first_name,
                    last_name=last_name,
                    # last_name=" ".join(last_name),
                    address=address,
                    # phone = phone,
                    created=now_utc,
                    modified=now_utc,
                    website_id=website_id

                )
                customer.save()
                buffer_data = common_functions.getAutoResponder("", "", "", "", "", 24)
                if buffer_data and buffer_data["content"]:
                    autoResponderData = buffer_data["content"]
                if autoResponderData["email_type"] == 'H':
                    emailContent = autoResponderData["email_content"]
                else:
                    emailContent = autoResponderData["email_content_text"]
                emailContent = str(emailContent)
                emailContent = emailContent.replace('{@first_name}', first_name)
                emailContent = emailContent.replace('{@email}', user_email)
                # emailContent = emailContent.replace('{@phone}',phone)
                if User:
                    emailcomponent.OrderMail(user_email, autoResponderData["email_from"], autoResponderData["subject"],
                                             emailContent)
                    str_status = status.HTTP_200_OK
                    # if device_id is not None and token is not None:
                    if device_id is not None:
                        rs_up = EngageboostTemporaryShoppingCarts.objects.filter(device_id=device_id,
                                                                                 customer_id__isnull=True).update(
                            customer_id=User.id)

                    data = {
                        'status': str_status,
                        'message': 'you have successfully signed up, phone number verification is pending',
                        # 'message': 'you have successfully signed up.',
                        'data': user_data
                    }

        except Exception as error:
            trace_back = sys.exc_info()[2]
            line = trace_back.tb_lineno
            str_status = status.HTTP_417_EXPECTATION_FAILED
            data = {"status": str_status, "api_status": traceback.format_exc(), "error_line": line,
                    "error_message": str(error), "message": str(error)}
        return Response(data, str_status)
#-----Test-----#

class CheckEmail(APIView):
    permission_classes = []
    def post(self, request, format=None):
        requestdata     = JSONParser().parse(request)
        username   = requestdata['username']
        try:
            if username!= '':
                ckeckingcnt=EngageboostUsers.objects.filter(Q(email__iexact=username) | Q(username=username)).count() 
        
                if ckeckingcnt>0:
                    str_status = status.HTTP_200_OK 
                    data = {
                    'status':str_status,
                    'message': 'This email / username already exists.'
                    }
               
                else:
                    str_status = status.HTTP_204_NO_CONTENT
                    data = {
                    'status':str_status,
                    'message': 'This email / username not exists.'
                    }
            else:
                str_status = status.HTTP_204_NO_CONTENT
                data = {
                    'status':str_status,
                    'message': 'This email / username is required.'
                    }
        except Exception as error:
                trace_back = sys.exc_info()[2]
                line = trace_back.tb_lineno
                str_status = status.HTTP_417_EXPECTATION_FAILED
                data = {"status": str_status, "api_status": traceback.format_exc(), "error_line": line, "error_message": str(error),"message": str(error,str_status)}
        return Response (data,str_status)


class SocialLogin(APIView):
    permission_classes = []
    def post(self, request, format=None):
        requestdata = JSONParser().parse(request)
        google_login_id = requestdata['google_login_id']
        facebook_id     = requestdata['facebook_id']
        user_email      = requestdata['user_email']
        first_name      = requestdata['first_name']
        last_name       = requestdata['last_name']
        phone           = requestdata['phone']
        image_name      = requestdata['image_name']
        device_id       = request.META.get('HTTP_DEVICEID')
        website_id      = request.META.get('HTTP_WID')
        now_utc = datetime.datetime.now(datetime.timezone.utc).astimezone()
        # if name:
        #     first_name, *last_name = name.split()
        space_index = user_email.split("@")[0]
        number = '{:03d}'.format(random.randrange(1, 999))
        username = (space_index + number)
        if website_id is None:
            website_id = 1
        if website_id<=0:
            website_id = 1
        try:
            if (google_login_id or facebook_id)=='':
                raise Exception("please provide google_login_id / facebook_id") 
            if (user_email or phone)=='':
                raise Exception("please provide email / phone")   
                
            if user_email!='':
                UserCke=EngageboostUsers.objects.filter(email__iexact=user_email,isblocked='n',isdeleted='n').first()
                customerCke=EngageboostCustomers.objects.filter(email__iexact=user_email,isdeleted='n').first()
            else:
                UserCke=EngageboostUsers.objects.filter(phone=phone,isblocked='n',isdeleted='n').first()
                customerCke=EngageboostCustomers.objects.filter(phone=phone,isdeleted='n').first()
            
            if UserCke and customerCke:
                # custBlock= EngageboostCustomers.objects.filter(Q(email__iexact=user_email) | Q(phone=phone)).filter(isdeleted='n',isblocked ='y').all()
                custBlock= EngageboostCustomers.objects.filter(Q(email__iexact=user_email)).filter(isdeleted='n',isblocked ='y').all()
                if custBlock:
                    raise Exception('Your account has been blocked.')
                User=EngageboostUsers.objects.filter(email__iexact=user_email,isdeleted='n',isblocked='n').latest('id')
                token=Token.objects.get_or_create(user=User)
                user_update = EngageboostUsers.objects.filter(isblocked='n',isdeleted='n',id=User.id).update(google_login_id=google_login_id,image_name=image_name,website_id=website_id)
                customer_update = EngageboostCustomers.objects.filter(isblocked='n',isdeleted='n',auth_user_id=User.id).update(facebook_id=facebook_id,website_id=website_id)
                user_data = EngageboostUsersSerializers(User).data
                token=Token.objects.get_or_create(user=User)
                auth = Token.objects.filter(user_id=User.id).latest('user_id')
                token = auth.key
                user_data.update({'token':token})
                user_data.update({'login-type':'google' if google_login_id else 'facebook'})
                if UserCke and customerCke:
                    str_status = status.HTTP_200_OK
                    if device_id is not None and token is not None:
                        rs_up = EngageboostTemporaryShoppingCarts.objects.filter(device_id=device_id, customer_id__isnull=True).update(customer_id=User.id)
                    
                    # Update Last Login
                    rs_user = EngageboostUsers.objects.filter(id = User.id).update(last_login=now_utc)

                    data = {
                    'status':str_status,
                    'message': 'you have successfully login.',
                    'data':user_data
                    }

            else:
                User=EngageboostUsers.objects.create(
                    email = user_email, 
                    username = username,
                    first_name = first_name,
                    last_name=last_name,
                    phone = phone,
                    date_joined = now_utc,
                    company_id = 1,
                    google_login_id = google_login_id,
                    image_name = image_name,
                    created_date = now_utc,
                    modified_date = now_utc,
                    user_type='frontend',
                    website_id=website_id
                )
                User.save()
                user_data = EngageboostUsersSerializers(User).data
                token=Token.objects.get_or_create(user=User)
                auth = Token.objects.filter(user_id=User.id).first()
                token = auth.key
                user_data.update({'token':token}) 
            
                customer=EngageboostCustomers.objects.create(
                    auth_user_id = User.id,
                    email = user_email, 
                    first_name = first_name,
                    last_name=last_name,
                    phone = phone,
                    facebook_id = facebook_id,
                    created = now_utc,
                    modified = now_utc,
                    website_id=website_id
                )
                customer.save()
                if User:
                    str_status = status.HTTP_200_OK
                    if device_id is not None and token is not None:
                        rs_up = EngageboostTemporaryShoppingCarts.objects.filter(device_id=device_id, customer_id__isnull=True).update(customer_id=User.id)
                    
                    # Update Last Login
                    rs_user = EngageboostUsers.objects.filter(id = User.id).update(last_login=now_utc)
                    data = {
                        'status':str_status,
                        'message': 'you have successfully signed up.',
                        'data':user_data
                        }
               
        except Exception as error:
            trace_back = sys.exc_info()[2]
            line = trace_back.tb_lineno
            str_status = status.HTTP_417_EXPECTATION_FAILED
            data = {"status": str_status, "api_status": traceback.format_exc(), "error_line": line, "error_message": str(error),"message": str(error)}
        return Response (data,str_status)


class AppleLogin(APIView):
    permission_classes = []
    def post(self, request, format=None):
        from pytz import timezone
        requestdata = JSONParser().parse(request)
        apple_login     = requestdata['apple_login']
        user_email      = requestdata['user_email']
        first_name      = requestdata['first_name']
        last_name       = requestdata['last_name']
        device_id       = request.META.get('HTTP_DEVICEID')
        website_id      = request.META.get('HTTP_WID')
        now_utc = datetime.datetime.now(timezone('UTC'))
        # if name:
        #     first_name, *last_name = name.split()
        user_email = user_email.strip()
        space_index = user_email.split("@")[0]
        number = '{:03d}'.format(random.randrange(1, 999))
        username = (space_index + number)
  
        try:
            if apple_login=='':
                raise Exception("please provide apple_login") 
            # if (user_email or phone)=='':
            #     raise Exception("please provide email / phone")   
            isExist = False   
            #isblock = False
            if user_email!='' and EngageboostCustomers.objects.filter(email__iexact=user_email,isdeleted='n').exists():  
                #print('if')
                # customerCke=EngageboostCustomers.objects.filter(email__iexact=user_email,isdeleted='n').count()   
                # update and login
                isExist = True
                #block check
                custBlock= EngageboostCustomers.objects.filter(email__iexact=user_email).filter(isdeleted='n',isblocked ='y').all()
                if custBlock:
                    raise Exception('Your account has been blocked.')
                else:
                    
                    customer_update = EngageboostCustomers.objects.filter(isblocked='n',isdeleted='n',email__iexact=user_email).update(ext_txt1=apple_login,website_id=website_id)
                    user_update = EngageboostUsers.objects.filter(isblocked='n',isdeleted='n',email__iexact=user_email,user_type ='frontend').update(website_id=website_id)
                    User=EngageboostUsers.objects.filter(email__iexact=user_email,isdeleted='n',isblocked='n',user_type ='frontend').latest('id')
                    token=Token.objects.get_or_create(user=User)
                    user_data = EngageboostUsersSerializers(User).data
                    token=Token.objects.get_or_create(user=User)
                    auth = Token.objects.filter(user_id=User.id).latest('user_id')
                    token = auth.key
                    user_data.update({'token':token})
                    #print('token',token)
                    str_status = status.HTTP_200_OK
                    if device_id is not None and token is not None:
                        rs_up = EngageboostTemporaryShoppingCarts.objects.filter(device_id=device_id, customer_id__isnull=True).update(customer_id=User.id)

                    # Update Last Login
                    rs_user = EngageboostUsers.objects.filter(id = User.id).update(last_login=now_utc)
                    
                    data = {
                    'status':str_status,
                    'message': 'you have successfully login.',
                    'data':user_data
                    }

            elif user_email!='' and not EngageboostCustomers.objects.filter(email__iexact=user_email,isdeleted='n').exists():
                # print('+++++++++',user_email)
                # print('elif')
                # create
                #print('create')
                isExist = True
                User=EngageboostUsers.objects.create(
                    email = user_email, 
                    username = username,
                    first_name = first_name,
                    last_name=last_name,
                    date_joined = now_utc,
                    company_id = 1,
                    created_date = now_utc,
                    modified_date = now_utc,
                    user_type='frontend',
                    website_id=website_id
                )
                User.save()
                user_data = EngageboostUsersSerializers(User).data
                token=Token.objects.get_or_create(user=User)
                auth = Token.objects.filter(user_id=User.id).first()
                token = auth.key
                user_data.update({'token':token}) 
                #user_data.update({'login-type':'google' if google_login_id else 'facebook'})
                customer=EngageboostCustomers.objects.create(
                    auth_user_id = User.id,
                    email = user_email, 
                    first_name = first_name,
                    last_name=last_name,
                    ext_txt1=apple_login,
                    created = now_utc,
                    modified = now_utc,
                    website_id=website_id
                    
                )
                customer.save()
                if User:
                    str_status = status.HTTP_200_OK
                    if device_id is not None and token is not None:
                        rs_up = EngageboostTemporaryShoppingCarts.objects.filter(device_id=device_id, customer_id__isnull=True).update(customer_id=User.id)

                    # Update Last Login
                    rs_user = EngageboostUsers.objects.filter(id = User.id).update(last_login=now_utc)
                    data = {
                        'status':str_status,
                        'message': 'you have successfully signed up.',
                        'data':user_data
                        }

            if not isExist and apple_login !='' and EngageboostCustomers.objects.filter(ext_txt1=apple_login,isdeleted='n').exists():
                
                # check login or not
                custBlock= EngageboostCustomers.objects.filter(ext_txt1=apple_login).filter(isdeleted='n',isblocked ='y').all()
                #print(custBlock.query)
                if custBlock:
                    raise Exception('Your account has been blocked.')
                else:
                    apple_login_exit = EngageboostCustomers.objects.filter(isdeleted='n',isblocked='n',ext_txt1=apple_login).first()
                    
                    customer_update = EngageboostCustomers.objects.filter(isblocked='n',isdeleted='n',ext_txt1=apple_login).update(website_id=website_id)
                    user_update = EngageboostUsers.objects.filter(isblocked='n',isdeleted='n',id=apple_login_exit.auth_user_id,user_type ='frontend').update(website_id=website_id)
                    User=EngageboostUsers.objects.filter(id=apple_login_exit.auth_user_id,isdeleted='n',isblocked='n',user_type ='frontend').latest('id')
                    token=Token.objects.get_or_create(user=User)
                    user_data = EngageboostUsersSerializers(User).data
                    token=Token.objects.get_or_create(user=User)
                    auth = Token.objects.filter(user_id=User.id).latest('user_id')
                    token = auth.key
                    user_data.update({'token':token})
                    #print('token',token)
                    str_status = status.HTTP_200_OK
                    if device_id is not None and token is not None:
                        rs_up = EngageboostTemporaryShoppingCarts.objects.filter(device_id=device_id, customer_id__isnull=True).update(customer_id=User.id)

                    # Update Last Login
                    rs_user = EngageboostUsers.objects.filter(id = User.id).update(last_login=now_utc)
                    
                    data = {
                    'status':str_status,
                    'message': 'you have successfully login.',
                    'data':user_data
                    }
            elif not isExist and not EngageboostCustomers.objects.filter(ext_txt1=apple_login,isdeleted='n').exists():
                str_status = status.HTTP_200_OK
                data = {
                    'status':str_status,
                    'message': 'apple loginid not exists ',
                    'data':{}
                    }
            
               
        except Exception as error:
            trace_back = sys.exc_info()[2]
            line = trace_back.tb_lineno
            str_status = status.HTTP_417_EXPECTATION_FAILED
            data = {"status": str_status, "api_status": traceback.format_exc(), "error_line": line, "error_message": str(error),"message": str(error)}
        return Response (data)