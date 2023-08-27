# import django packages
from django.urls import path
from django.conf.urls import url, include
from django.contrib import admin
from rest_framework import routers

# import apis
from api.views import views_blog

"""
Blogs infomation and blog CRUD
"""


# router = routers.DefaultRouter()
# router.register(r'xxx', views_user_crud.EmployeeTest)

urlpatterns = [
    url(r"^(?P<version>[v1|v2]+)/blogs/$", views_blog.BlogsView.as_view()),
    url(r"^(?P<version>[v1|v2]+)/upload_images/$", views_blog.UploadImgaesView.as_view()),
    url(r"^(?P<version>[v1|v2]+)/likes_check/$", views_blog.BlogLikeCheckView.as_view()),
    url(r"^(?P<version>[v1|v2]+)/like/$", views_blog.BlogLikeView.as_view()),
    url(r"^(?P<version>[v1|v2]+)/unlike/$", views_blog.BlogUnlikeView.as_view()),
    url(r"^(?P<version>[v1|v2]+)/publish/$", views_blog.BlogPublishView.as_view()),
    url(r"^(?P<version>[v1|v2]+)/edit/$", views_blog.BlogEditView.as_view()),
    url(r"^(?P<version>[v1|v2]+)/delete/$", views_blog.DeleteBlogView.as_view()),
    url(r"^(?P<version>[v1|v2]+)/search/$", views_blog.SearchBlogByKeywordsView.as_view()),
    url(r"^(?P<version>[v1|v2]+)/search_blog_by_id/$", views_blog.SearchBlogByIdView.as_view()),
    # url(r"^(?P<version>[v1|v2]+)/user_info/(?P<pk>\d+)$", views_user.UserInfomationSearchView.as_view()),
    # url(r"^(?P<version>[v1|v2]+)/user_info_list/$", views_user.UserProfileListView.as_view({"get": "list", "delete": "destroy", "put": "update", "patch": "partial_update"})),
]

# urlpatterns += router.urls
