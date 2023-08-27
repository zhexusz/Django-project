from models.models import models_user
from rest_framework import exceptions, permissions
from django.http import HttpResponse, JsonResponse
import json

class IsAdminUser(permissions.BasePermission):
    def has_permission(self, request, view):
        user_id = request.userId[0]  # get user id from token
        user_check = models_user.UserInfo.objects.filter(userId=user_id).first()

        # if user not found
        if not user_check:
            raise exceptions.AuthenticationFailed("User not found")

        # if user found, check if user is admin
        if user_check.userRole == "admin":  # if user is admin, return True
            return True
        else:
            return False


# class AllowAnyUser(permissions.BasePermission):
#     def has_permission(self, request, view):
#         return True


# class Authentication(object):
#     def authenticate(self, request):
#         token = json.loads(request.body).get("token")  # token

#         print("Token is:", token)
#         token_obj = models_user.UserLogin.objects.filter(token=token).first()
#         if not token_obj:
#             raise exceptions.AuthenticationFailed("Authentication Failed")
#         return (token_obj.userId, token_obj)

#     def authenticate_header(self, request):
#         pass

from datetime import datetime

class Authentication(object):
    def authenticate(self, request):
        token = json.loads(request.body).get("token")  # token
        print("Token is:", token)
        token_obj = models_user.UserLogin.objects.filter(token=token).first()
        if not token_obj:
            raise exceptions.AuthenticationFailed("Authentication Failed")
        
        # Check if the token is expired
        if token_obj.is_expired():
            token_obj.delete()
            raise exceptions.NotAcceptable("Token is expired", code=406)

        return (token_obj.userId, token_obj)

    def authenticate_header(self, request):
        pass