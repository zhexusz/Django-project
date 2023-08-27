# import django packages
from django.urls import path
from django.conf.urls import url, include
from django.contrib import admin
from rest_framework import routers

# import apis
from api.views import views_pet

"""
Pets information and pets CRUD
"""


urlpatterns = [
    url(r"^(?P<version>[v1|v2]+)/list/$", views_pet.PetInfoListView.as_view()),
    url(r"^(?P<version>[v1|v2]+)/info/$", views_pet.PetInfoView.as_view()),
    url(r"^(?P<version>[v1|v2]+)/edit/$", views_pet.PetInfoEditView.as_view()),
    url(r"^(?P<version>[v1|v2]+)/add/$", views_pet.AddPetView.as_view()),
    url(r"^(?P<version>[v1|v2]+)/delete/$", views_pet.PetInfoDeleteView.as_view()),
    # url(r"^(?P<version>[v1|v2]+)/user_info/(?P<pk>\d+)$", views_pet.UserInfomationSearchView.as_view()),
    # url(r"^(?P<version>[v1|v2]+)/user_info_list/$", views_pet.UserProfileListView.as_view({"get": "list", "delete": "destroy", "put": "update", "patch": "partial_update"})),
]

# urlpatterns += router.urls
