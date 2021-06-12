from django.shortcuts import render

from rest_framework import generics, permissions, status, views, mixins
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response

# Import Model And Serializer
from webservices.models import *
from coremodule.coremodule_serializers import *

import json
import base64
# import hashlib
# from Crypto import Random
# from Crypto.Cipher import AES
# from pkcs7 import PKCS7Encoder

# print(json.dumps(jsn, indent=4, sort_keys=True))