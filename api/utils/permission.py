from rest_framework.permissions import BasePermission
from django.http import JsonResponse
from django.http import HttpResponse


class BasicUser(BasePermission):
    
    def has_permission(self,request,view):
        if request.user.user_type == 3:
            return False
        return True
    # def authenticate_header(self, request):
    #     pass

class AdminUser(BasePermission):
    message = "Here is admin user permission"
    def has_permission(self,request,view):
        if request.user.user_type != 3:
            return False
        return True