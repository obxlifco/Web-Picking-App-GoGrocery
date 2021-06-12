# -------------------LOGIN SIGNUP--------------
from webservices.views.loginview import login
from webservices.views.loginview import insertdata
from webservices.views.createuser import usercreate,createotp,checkotp
from webservices.views.forgotpassword import forgotpassword,verification
from webservices.views.changepassword import changepassword


# -------------------LOGIN SIGNUP--------------
# -------------------MENU--------------
from webservices.views.MasterMenu import MenuViewSet
from webservices.views.MasterMenu_group import MenuGroup
# -------------------MENU--------------

# -------------------Elastic Search--------------
from webservices.views.Elasticsearch import ESMenuViewSet
from webservices.views.Elasticsearch import ESMenuActionViewSet,ESDataActionViewSet,ModifySku,ESsearchdata
# -------------------Elastic Search--------------
from webservices.views.routers import DB

import warnings
 




