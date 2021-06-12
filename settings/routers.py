from django.conf import settings
import os
import socket
from django.http import *
from django.db.models import *
import requests
from django.http import HttpResponse
from rest_framework import generics,viewsets
from rest_framework.response import Response


class DB(generics.ListAPIView):
    
    def POST(self,model,**hints):
        from boost.models import EngageboostCompanies
        print(socket.gethostbyname(socket.gethostname()))
        host = socket.gethostbyname(socket.gethostname())

        user = EngageboostCompanies.objects.get(db_host=host)
        # print(user.query)




class DatabaseRouter(object):
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    
    print(1)
        
    """
    A router to control all database operations on models for different
    databases.
    """
    def db_for_read(self, model, **hints):
        """"Point all read operations to the specific database."""
        # print(os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)))
        # print(socket.gethostbyname(self))
        # current_site = Site.objects.get_current()
        # print(model._meta.HTTP_HOST)
        # url=request.META['HTTP_HOST']
        print(1)
        if 'localhost:8000'=='localhost:8000':
            # DATABASES = {
            #     'external_db' : {
            #         'ENGINE': 'django.db.backends.postgresql_psycopg2',
            #         'NAME': 'boostv2',
            #         'USER': 'postgres',
            #         'PASSWORD': 'navsoftpsql',
            #         'HOST': '192.168.0.65',
            #         'PORT': '',
            #     }
            # }
            
            from boost.models import EngageboostCompanies
            print(socket.gethostbyname(socket.gethostname()))
            host = socket.gethostbyname(socket.gethostname())

            user = EngageboostCompanies.objects.get(db_host=host)
            print(user.query)
            
        else:
            from boost.models import EngageboostCompanies
            # print(socket.gethostbyname(socket.gethostname()))
            host = socket.gethostbyname(socket.gethostname())

            user = EngageboostCompanies.objects.get(db_host=host)
            print(user.query)
            
        return 'web'
 
    def db_for_write(self, model, **hints):
        """Point all write operations to the specific database."""
        # if request.META['HTTP_HOST']=='localhost:8000':
        if 'localhost:8000'=='localhost:8000':
            DATABASES = {
                'external_db' : {
                    'ENGINE': 'django.db.backends.postgresql_psycopg2',
                    'NAME': 'boostv2',
                    'USER': 'postgres',
                    'PASSWORD': 'navsoftpsql',
                    'HOST': '192.168.0.65',
                    'PORT': '',
                }
            }
            from boost.models import EngageboostCompanies
            # print(socket.gethostbyname(socket.gethostname()))
            host = socket.gethostbyname(socket.gethostname())

            user = EngageboostCompanies.objects.get(db_host=host)
            print(user.query)
            
            
        else:
            from boost.models import EngageboostCompanies
            # print(socket.gethostbyname(socket.gethostname()))
            host = socket.gethostbyname(socket.gethostname())

            user = EngageboostCompanies.objects.get(db_host=host)
            print(user.query)
            
            
        return 'web'

        # def allow_migrate(db, app_label):
    #         # if(db == "locations_db"):
    #         #     return model._meta.app_label == 'locations'
    #         # elif model._meta.app_label == 'locations':
    #         #     return False
    #         # else:
    #         #     return None
    #         return None    
    # def allow_relation(self, obj1, obj2, **hints):
    #     """Allow any relation between apps that use the same database."""
    #     db_obj1 = settings.DATABASE_APPS_MAPPING.get(obj1._meta.app_label)
    #     db_obj2 = settings.DATABASE_APPS_MAPPING.get(obj2._meta.app_label)
    #     if db_obj1 and db_obj2:
    #         if db_obj1 == db_obj2:
    #             return True
    #         else:
    #             return False
    #     return None
 
    # def allow_syncdb(self, db, model):
    #     """Make sure that apps only appear in the related database."""
    #     if db in settings.DATABASE_APPS_MAPPING.values():
    #         return settings.DATABASE_APPS_MAPPING.get(model._meta.app_label) == db
    #     elif settings.DATABASE_APPS_MAPPING.has_key(model._meta.app_label):
    #         return False
    #     return None

        # port2 = socket.gethostbyname(socket.gethostname())