"""
petopia URL Configuration
"""
from django.contrib import admin
from django.urls import path
from django.conf.urls import url, include

from api.urls import urls_user
from api.urls import urls_blog
from api.urls import urls_pet
from api.urls import urls_map

from django.conf import settings
from django.conf.urls.static import static
from django.views.static import serve

# from background_task import urls as background_urls


# from api.views import views_user_login

urlpatterns = [
    path("admin/", admin.site.urls),
    # url(r'^api/v1/auth/$', views_user_login.EmployeeLoginAuth.as_view()),
    url(r"^api/user/", include("api.urls.urls_user")),
    url(r"^api/blog/", include("api.urls.urls_blog")),
    url(r"^api/pet/", include("api.urls.urls_pet")),
    url(r"^api/map/", include("api.urls.urls_map")),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# background task
# urlpatterns += background_urls.urlpatterns
