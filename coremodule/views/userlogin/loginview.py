from django.http import HttpResponse
from django.conf.urls import include, url
from django.views.decorators.csrf import csrf_exempt, ensure_csrf_cookie
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.hashers import make_password, check_password
from django.utils.decorators import method_decorator
from django.contrib.auth import get_user_model, login, authenticate
from django.db.models import Q
# from django.db.models.signals import post_save
# from django.dispatch import receiver
from django.http import JsonResponse
from django.conf import settings

from webservices.models import *
from webservices.views import loginview

from validate_email import validate_email
from bcrypt import hashpw, gensalt
from rest_framework import generics, permissions, status, views, mixins
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from rest_framework.authentication import TokenAuthentication, BasicAuthentication, SessionAuthentication
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.views import APIView
from rest_framework.exceptions import ParseError
from rest_framework.authtoken.models import Token
# from coremodule.views.enc import *
from django.utils import timezone
from urllib.request import urlopen
import json
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import uuid


@csrf_exempt
def login(request):
    requestdata = JSONParser().parse(request)
    user_mail = requestdata['username']
    user_passw = requestdata['password']
    ip = requestdata['ip_address']

    objUser = EngageboostUsers.objects.filter(Q(username=user_mail) | Q(
        email=user_mail)).filter(isdeleted='n').first()
    cnt = 0
    if objUser:
        cnt = 1

    if cnt <= 0:
        data = {
            'status': 0,
            'message': 'Username / password mismatch.'
        }
        return JsonResponse(data)
    else:
        password_check = objUser.check_password(user_passw)
        token, created = Token.objects.get_or_create(user=objUser)
        token_data = token.key

        if password_check:
            if(objUser.is_verified == 'n'):
                data = {
                    'status': 0,
                    'message': 'User not verified.'
                }
            elif(objUser.isblocked == 'y'):
                data = {
                    'status': 0,
                    'message': 'Your account is blocked. If you want to activate it please contact administrator.'
                }
            else:
                EngageboostUsers.objects.filter(email=user_mail).update(
                    last_login=datetime.now(), ip_address=ip)
                userdata = {
                    'first_name': objUser.first_name,
                    'last_name': objUser.last_name,
                    'token': token_data,
                    'user_id': objUser.id,
                    'email': objUser.email
                }

                data = {
                    'status': 1,
                    'msg': 'success',
                    'user_data': userdata,
                }
        else:
            data = {
                'status': 0,
                'message': 'Username / password mismatch.'
            }
        return JsonResponse(data)


@csrf_exempt
def signup(request):
    if request.method == "POST":
        requestdata = JSONParser().parse(request)
        email = requestdata['email']
        name = requestdata['name']
        mobile = requestdata['mobile']
        password = requestdata['password']
        hash_password = make_password(password, None, 'md5')

        cnt_User = EngageboostUsers.objects.filter(email=email).count()
        if(cnt_User == 0):
            user_n = email.split("@")
            cnt_Username = EngageboostUsers.objects.filter(
                username=user_n).count()
            if(cnt_Username == 0):
                username = user_n[0]
            else:
                pin = str(random.randint(11111, 99999))
                username = user_n[0] + pin

            state, city, pincode = getplace(
                requestdata['latitude'], requestdata['longitude'])

            verfi_code = str(uuid.uuid4())[:30]
            objuser = EngageboostUsers.objects.create(
                email=email,
                password=hash_password,
                username=username,
                first_name=name,
                is_superuser=False,
                is_staff=False,
                is_active=True,
                created_date=timezone.now(),
                isblocked='n',
                isdeleted='n',
                is_verified='n',
                date_joined=timezone.now(),
                issuperadmin='N',
                user_type='frontend',
                phone=mobile,
                state=state,
                city=city,
                postcode=pincode,
                verified_code=verfi_code,
                modified_date=timezone.now()
            )
            objuser.save()
            objCust = EngageboostCustomers.objects.create(
                first_name=name,
                email=email,
                password=hash_password,
                phone=mobile,
                created=timezone.now(),
                isblocked='n',
                isdeleted='n',
                is_import='n',
                auth_user_id=objuser.id,
                modified=timezone.now()
            )
            objCust.save()

            email_from = settings.EMAIL_HOST_USER

            # Create message container - the correct MIME type is multipart/alternative.
            msg = MIMEMultipart('alternative')
            msg['Subject'] = "Email Verification"
            msg['From'] = email_from
            msg['To'] = email

            # Create the body of the message (a plain-text and an HTML version).
            template = 'Hello User, <br/><br/>Click <a href="' + str(settings.SITE_URL) + '/api/common/email_verify/' + \
                str(verfi_code) + \
                '">here </a>to verify email <br/><br/>Regards,<br/>Navsoft'

            # Record the MIME types of both parts - text/plain and text/html.
            msg_content = MIMEText(template, 'html')
            msg.attach(msg_content)
            # Send the message via local SMTP server.
            mail = smtplib.SMTP(settings.EMAIL_HOST, settings.EMAIL_PORT)
            mail.ehlo()
            mail.starttls()
            mail.login(email_from, settings.EMAIL_HOST_PASSWORD)
            mail.sendmail(email_from, email, msg.as_string())
            mail.quit()
            data = {
                'status': 1,
                'message': 'User Created Successfully.'
            }
        else:
            data = {
                'status': 0,
                'message': 'Email Already Exists.'
            }
    else:
        data = {
            'status': 0,
            'message': 'Invalid request.'
        }
    return JsonResponse(data)


def getplace(lat, lon):
    try:
        print(lat, lon)
        url = "https://maps.googleapis.com/maps/api/geocode/json?latlng=%s,%s&key=AIzaSyD5FbqPZaL1phvv3ZouQUGK-yI08QHSvLs&sensor=false" % (
            lat, lon)
        v = urlopen(url).read()
        j = json.loads(v)
        print(j)
        state = ""
        city = ""
        pincode = ""
        components = j['results'][0]['address_components']
        print(components)
        # country = town = None
        for c in components:
            if "postal_code" in c['types']:
                pincode = c['postal_code']
            if "administrative_area_level_1" in c['types']:
                state = c['administrative_area_level_1']
            if "administrative_area_level_2" in c['types']:
                city = c['administrative_area_level_2']
        return state, city, pincode
    except Exception as ex:
        print(ex)
        return "", "", ""


@csrf_exempt
def email_verify(request, str_code):
    if(str_code):
        cnt_User = EngageboostUsers.objects.filter(
            verified_code=str_code).count()
        if(cnt_User == 0):
            data = {
                "status": 0,
                "message": "Invalid verification code."
            }
        else:
            obj_User = EngageboostUsers.objects.get(verified_code=str_code)
            if(obj_User.is_verified == 'y'):
                data = {
                    "status": 0,
                    "message": "User already verified."
                }
            else:
                obj_User.is_verified = 'y'
                obj_User.save()
                data = {
                    "status": 1,
                    "message": "User verified successfully."
                }
    else:
        data = {
            "status": 0,
            "message": 'Invalid request.'
        }
    return JsonResponse(data)
