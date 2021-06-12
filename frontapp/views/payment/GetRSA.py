# importing the requests library 
import requests 
from django.views.decorators.csrf import csrf_exempt, ensure_csrf_cookie
from rest_framework.response import Response
from django.http import JsonResponse
from django.http import HttpResponse, HttpResponseRedirect
from rest_framework.parsers import JSONParser
import json

@csrf_exempt
def GetRsa(request):
        if(request.method == "GET"):
                print("***************", request.GET)
                # defining the url 
                url = "https://secure.ccavenue.ae/transaction/getRSAKey"
                orderid = request.GET['order_id']
                print("orderid=======", orderid)
                # your Access Code and Order ID 
                # access_code = "AVUQ03GK18BR25QURB"  #put access code here
                # order_id = "test123"                #provide your order id here
                access_code = "AVUP03GL28CI81PUIC"
                order_id = orderid

                # data to be sent to url 
                data = {'access_code':access_code, 
                        'order_id':order_id} 

                # sending post request and saving response as response object 
                r = requests.post(url = url, data = data) 

                # extracting response text 
                url_response = r.text 
                print(url_response)
                data = {
                        "data":url_response
                }
                return HttpResponse(url_response)
        elif (request.method == "POST"):
                data = request.POST
                url = "https://secure.ccavenue.ae/transaction/getRSAKey"
                orderid = data['order_id']
                # your Access Code and Order ID 
                # access_code = "AVUP03GL28CI81PUIC"        # Demo
                access_code = "AVZO03HA32BC46OZCB"        # Live
                order_id = orderid
                # data to be sent to url 
                data = {'access_code':access_code, 
                        'order_id':order_id
                       } 

                # sending post request and saving response as response object 
                r = requests.post(url = url, data = data) 
                # extracting response text 
                url_response = r.text 
                data = {
                        "data":url_response
                }
                print("RSA VALUE++++++++++++++++++", url_response)
                return HttpResponse(url_response)

@csrf_exempt
def GetRsaDemo(request):
        if(request.method == "GET"):
                print("***************", request.GET)
                # defining the url 
                url = "https://secure.ccavenue.ae/transaction/getRSAKey"
                orderid = request.GET['order_id']
                print("orderid=======", orderid)
                # your Access Code and Order ID 
                # access_code = "AVUQ03GK18BR25QURB"  #put access code here
                # order_id = "test123"                #provide your order id here
                access_code = "AVUP03GL28CI81PUIC"
                order_id = orderid

                # data to be sent to url 
                data = {'access_code':access_code, 
                        'order_id':order_id} 

                # sending post request and saving response as response object 
                r = requests.post(url = url, data = data) 

                # extracting response text 
                url_response = r.text 
                print(url_response)
                data = {
                        "data":url_response
                }
                return HttpResponse(url_response)
        elif (request.method == "POST"):
                data = request.POST
                print("data==", data)
                url = "https://secure.ccavenue.ae/transaction/getRSAKey"
                orderid = data['order_id']
                # your Access Code and Order ID 
                access_code = "AVCG03HF47CJ43GCJC"        # Demo SI
                # access_code = "AVUP03GL28CI81PUIC"        # Demo
                # access_code = "AVZO03HA32BC46OZCB"        # Live
                order_id = orderid
                # data to be sent to url 
                data = {'access_code':access_code, 
                        'order_id':order_id
                       } 

                # sending post request and saving response as response object 
                r = requests.post(url = url, data = data) 
                # extracting response text 
                url_response = r.text 
                data = {
                        "data":url_response
                }
                print("RSA VALUE++++++++++++++++++", url_response)
                return HttpResponse(url_response)
# GetRsa()AVZO03HA32BC46OZCB

@csrf_exempt
def GetRsaSi(request):
        if(request.method == "GET"):
                print("***************", request.GET)
                # defining the url 
                url = "https://secure.ccavenue.ae/transaction/getRSAKey"
                orderid = request.GET['order_id']
                print("orderid=======", orderid)
                # your Access Code and Order ID 
                # access_code = "AVUQ03GK18BR25QURB"  #put access code here
                # order_id = "test123"                #provide your order id here
                # access_code = "AVUP03GL28CI81PUIC"
                access_code = "AVZO03HA32BC46OZCB"
                order_id = orderid

                # data to be sent to url 
                data = {'access_code':access_code, 
                        'order_id':order_id} 

                # sending post request and saving response as response object 
                r = requests.post(url = url, data = data) 

                # extracting response text 
                url_response = r.text 
                print(url_response)
                data = {
                        "data":url_response
                }
                return HttpResponse(url_response)
        elif (request.method == "POST"):
                data = request.POST
                print("data==", data)
                url = "https://secure.ccavenue.ae/transaction/getRSAKey"
                orderid = data['order_id']
                # your Access Code and Order ID 
                # access_code = "AVCG03HF47CJ43GCJC"        # Demo SI
                # access_code = "AVUP03GL28CI81PUIC"        # Demo
                access_code = "AVZO03HA32BC46OZCB"        # Live
                order_id = orderid
                # data to be sent to url 
                data = {'access_code':access_code, 
                        'order_id':order_id
                       } 

                # sending post request and saving response as response object 
                r = requests.post(url = url, data = data) 
                # extracting response text 
                url_response = r.text 
                data = {
                        "data":url_response
                }
                print("RSA VALUE++++++++++++++++++", url_response)
                return HttpResponse(url_response)
                