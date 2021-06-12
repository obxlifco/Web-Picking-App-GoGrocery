
# -------------------USER--------------
from webservices.views.employee.User import UserList,UserDetail,UserAction,RoleAssign,UserChangePassword,CustomerDataFetch
# -------------------USER--------------

# -------------------Groups--------------
from webservices.views.employee.Groups import GroupsList,GroupsDetail,GroupsAction,Active
# -------------------Groups--------------

# -------------------ROLE--------------
from webservices.views.employee.RoleMaster import RoleMasterViewSet,RoleMasterDetail,RoleList,Groupname,UsersName,GetRoleMenu,EditRole
# from webservices.views.employee.groupname import list_role
# -------------------ROLE--------------