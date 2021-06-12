from django.conf import settings
import os
import socket
from django.http import *
from django.db.models import *
import requests
from django.http import HttpResponse
from rest_framework import generics,viewsets
from rest_framework.response import Response
import json
from webservices.models import EngageboostCompanies
from settings import settings
import string
from boost import models
from django import db

def get_dbname():

    host = socket.gethostbyname(socket.gethostname())
    db_fetch = EngageboostCompanies.objects.get(db_host=str(host))
    external_db = {'ENGINE': 'django.db.backends.postgresql_psycopg2',
                            'NAME': 'boostv2','USER': 'postgres',
                            'PASSWORD': 'navsoftpsql',
                            'HOST': '192.168.0.65',
                            'PORT': ''}
    # settings.DATABASES['web'] = external_db                        
    # return db_fetch.database_name  

    # db='default': {
    #     'ENGINE': 'django.db.backends.postgresql_psycopg2',
    #     'NAME': 'boostv2',
    #     'USER': 'postgres',
    #     'PASSWORD': 'navsoftpsql',
    #     'HOST': '192.168.0.65',
    #     'PORT': '',
    # }
    return Response(1)


class DB(generics.ListAPIView):
    
    def post(self, request, format=None):

        host = socket.gethostbyname(socket.gethostname())

        db_fetch = EngageboostCompanies.objects.all()
        for fetch in db_fetch:
            settings.DATABASES[fetch.company_name]={'ENGINE':'django.db.backends.postgresql_psycopg2',
                                                    'NAME': fetch.database_name,
                                                    'USER': fetch.database_user_name,
                                                    'PASSWORD': fetch.database_password,
                                                    'HOST': fetch.db_host,
                                                    'PORT': ''}


            # external_db = {'ENGINE': 'django.db.backends.postgresql_psycopg2',
            #                     'NAME': 'pg_primemalltest','USER': 'postgres',
            #                     'PASSWORD': 'navsoftpsql',
            #                     'HOST': '192.168.0.65',
            #                     'PORT': ''}
            # settings.DATABASES['default'] = external_db
        return Response(settings.DATABASES)


def get_dname():

    host = socket.gethostbyname(socket.gethostname())
    db_fetch = EngageboostCompanies.objects.get(db_host=str(host))
    external_db = {'ENGINE': 'django.db.backends.postgresql_psycopg2',
                            'NAME': 'boostv2','USER': 'postgres',
                            'PASSWORD': 'navsoftpsql',
                            'HOST': '192.168.0.65',
                            'PORT': ''}
    settings.DATABASES['web'] = external_db                        
    # return db_fetch.database_name  
    return Response(settings.DATABASES['web'])


# class MyDB(object):
#     _db_connection = None
#     _db_cur = None

#     def __init__(self):
#         self._db_connection = db_module.connect('host', 'user', 'password', 'db')
#         self._db_cur = self._db_connection.cursor()

#     def query(self, query, params):
#         return self._db_cur.execute(query, params)

#     def __del__(self):
#         self._db_connection.close()


# class AppRouter(object):
#     # print(db.connections.databases)
#     print(get_dname())
#     def db_for_read(self, model, **hints):
#         print(get_dname())
#         settings.DATABASES['web']=get_dname()
#         return 'web'

#     def db_for_write(self, model, **hints):
#         settings.DATABASES['web']=get_dname()
#         return 'web'

#     def allow_migrate(self, db, app_label, model=None, **hints):    
#         settings.DATABASES['web']=get_dname()
#         return 'web'

class DatabaseRouter(object):

    # host = socket.gethostbyname(socket.gethostname())
    # db_fetch = EngageboostCompanies.objects.get(db_host=str(host))
    
        
    """
    A router to control all database operations on models for different
    databases.
    """
    # using = 'web'

    def db_for_read(self, model, **hints):
        """"Point all read operations to the specific database."""
        # print(os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)))
        # print(socket.gethostbyname(self))
        # current_site = Site.objects.get_current()
        # print(model._meta.HTTP_HOST)
        # url=request.META['HTTP_HOST']
        # host = socket.gethostbyname(socket.gethostname())
        
        # if host=='127.0.1.1':
        db=get_dname()
        external_db = {'ENGINE': 'django.db.backends.postgresql_psycopg2',
                        'NAME': 'boostv2',
                        'USER': 'postgres',
                        'PASSWORD': 'navsoftpsql',
                        'HOST': '192.168.0.65',
                        'PORT': ''
                       }
        # settings.DATABASES['web'] = external_db
        return 'web'
            # from boost.models import EngageboostCompanies
            # print(socket.gethostbyname(socket.gethostname()))
            # host = socket.gethostbyname(socket.gethostname())

            # user = EngageboostCompanies.objects.get(db_host=host)
            # print(user.query)
            
        # else:
        #     from boost.models import EngageboostCompanies
        #     # print(socket.gethostbyname(socket.gethostname()))
        #     host = socket.gethostbyname(socket.gethostname())

        #     user = EngageboostCompanies.objects.get(db_host=host)
        #     print(user.query)
            
        # return 'local'
 
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
            
            
        return 'local'

    def __del__(self):
        self._db_connection.close()

        def allow_migrate(db, app_label):
            # if(db == "locations_db"):
            #     return model._meta.app_label == 'locations'
            # elif model._meta.app_label == 'locations':
            #     return False
            # else:
            #     return None
            return None    
    def allow_relation(self, obj1, obj2, **hints):
        """Allow any relation between apps that use the same database."""
        db_obj1 = settings.DATABASE_APPS_MAPPING.get(obj1._meta.app_label)
        db_obj2 = settings.DATABASE_APPS_MAPPING.get(obj2._meta.app_label)
        if db_obj1 and db_obj2:
            if db_obj1 == db_obj2:
                return True
            else:
                return False
        return None
 
    def allow_syncdb(self, db, model):
        """Make sure that apps only appear in the related database."""
        if db in settings.DATABASE_APPS_MAPPING.values():
            return settings.DATABASE_APPS_MAPPING.get(model._meta.app_label) == db
        elif settings.DATABASE_APPS_MAPPING.has_key(model._meta.app_label):
            return False
        return None

        port2 = socket.gethostbyname(socket.gethostname())

