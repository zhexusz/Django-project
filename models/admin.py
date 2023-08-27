from django.contrib import admin
from models.models.models_blog import *
from models.models.models_map import *
from models.models.models_pet import *
from models.models.models_user import *

# Regist blogs
admin.site.register(BlogDetails)

# Regist map
admin.site.register(MapCourseInfo)
admin.site.register(MapSchoolInfo)
admin.site.register(MapVetInfo)

# Regist pets
admin.site.register(PetInfo)

# Regist users
admin.site.register(UserRole)
admin.site.register(UserInfo)
admin.site.register(UserLikes)
admin.site.register(UserFollows)
admin.site.register(UserLogin)
