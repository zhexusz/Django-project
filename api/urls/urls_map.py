# import django packages
from django.urls import path
from django.conf.urls import url, include
from django.contrib import admin
from rest_framework import routers

# import apis
from api.views import views_map

"""
Maps information
"""


# router = routers.DefaultRouter()
# router.register(r'xxx', views_user_crud.EmployeeTest)

urlpatterns = [
    url(r"^(?P<version>[v1|v2]+)/school/$", views_map.SchoolListView.as_view()),
    url(r"^(?P<version>[v1|v2]+)/add_school/$", views_map.AddSchoolView.as_view()),
    url(r"^(?P<version>[v1|v2]+)/vet_search/$", views_map.VetSearchView.as_view()),
    url(r"^(?P<version>[v1|v2]+)/vet/$", views_map.VetListView.as_view()),
    url(r"^(?P<version>[v1|v2]+)/add_vet/$", views_map.AddVetView.as_view()),
    url(r"^(?P<version>[v1|v2]+)/course/$", views_map.CourseListView.as_view()),
    url(r"^(?P<version>[v1|v2]+)/add_course/$", views_map.AddCourseView.as_view()),
    # url(r"^(?P<version>[v1|v2]+)/user_info/(?P<pk>\d+)$", views_user.UserInfomationSearchView.as_view()),
    # 门店信息管理
    # url(r"^(?P<version>[v1|v2]+)/user_info_list/$", views_user.UserProfileListView.as_view({"get": "list", "delete": "destroy", "put": "update", "patch": "partial_update"})),
]

# urlpatterns += router.urls
