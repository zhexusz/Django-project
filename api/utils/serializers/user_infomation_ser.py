from rest_framework import serializers
from models.models import models_user

# format: Viewname + Ser

# user profile serializer
class UserInfoSer(serializers.ModelSerializer):
    class Meta:
        model = models_user.UserInfo
        fields = "__all__"
