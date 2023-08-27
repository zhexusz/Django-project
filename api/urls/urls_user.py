# import django packages
from django.urls import path
from django.conf.urls import url, include
from django.contrib import admin
from rest_framework import routers

# import apis
from api.views import views_user

"""
User Profile and user CRUD, including:
1. User Profile
2. User CRUD
3. User Login
4. User Logout
5. User Register
6. User Change Password
7. Current User (for frontend to get current user info)
"""

# router = routers.DefaultRouter()
# router.register(r'xxx', views_user_crud.EmployeeTest)

urlpatterns = [
    url(r"^(?P<version>[v1|v2]+)/profile/$", views_user.UserProfileView.as_view()),
    url(r"^(?P<version>[v1|v2]+)/login/$", views_user.UserLoginAuthView.as_view()),
    url(r"^(?P<version>[v1|v2]+)/logout/$", views_user.UserLogoutView.as_view()),
    url(r"^(?P<version>[v1|v2]+)/register/$", views_user.UserCreateView.as_view()),
    url(r"^(?P<version>[v1|v2]+)/change_password/$", views_user.UserChangePasswordView.as_view()),
    url(r"^(?P<version>[v1|v2]+)/edit/$", views_user.UserInfoEditView.as_view()),
    url(r"^(?P<version>[v1|v2]+)/delete/$", views_user.UserDeleteView.as_view()),
    url(r"^(?P<version>[v1|v2]+)/follow/$", views_user.UserFollowView.as_view()),
    url(r"^(?P<version>[v1|v2]+)/unfollow/$", views_user.UserUnfollowView.as_view()),
    url(r"^(?P<version>[v1|v2]+)/current_user/$", views_user.CurrentUserView.as_view()),
    # url(r"^(?P<version>[v1|v2]+)/user_info/(?P<pk>\d+)$", views_user.UserProfileView.as_view()),
    # url(r"^(?P<version>[v1|v2]+)/user_info_list/$", views_user.UserProfileListView.as_view({"get": "list", "delete": "destroy", "put": "update", "patch": "partial_update"})),
]

# urlpatterns += router.urls
