from django.db import models
from datetime import datetime
from datetime import timedelta
from django.utils import timezone

"""
Models connected with databases
"""


# User role
class UserRole(models.Model):
    roleId = models.AutoField(primary_key=True, verbose_name="listId")  # listId
    roleName = models.CharField(max_length=200, verbose_name="roleId", default=None)  # roleId
    roleStatus = models.IntegerField(default=1, verbose_name="roleStatus")  # roleStatus

    def toDict(self):  # return as dict
        return {
            "roleId": self.roleId,
            "roleName": self.roleName,
            "roleStatus": self.roleStatus,
        }

    class Meta:
        db_table = "user_role"  # table name


# User Info
class UserInfo(models.Model):
    userId = models.AutoField(primary_key=True, verbose_name="userId")  # userId
    username = models.CharField(max_length=200, verbose_name="username", default=None)  # username
    email = models.CharField(max_length=200, verbose_name="email", default=None)  # email
    gender = models.CharField(max_length=200, verbose_name="gender", default=None, null=True, blank=True)  # gender
    userRole = models.ManyToManyField(UserRole, verbose_name="userRole")  # userRole
    createTime = models.DateTimeField(default=datetime.now)  # createTime
    selfIntroduction = models.CharField(max_length=2000, verbose_name="selfIntroduction", default=None, null=True, blank=True)  # selfIntroduction
    userStatus = models.IntegerField(default=1, verbose_name="userStatus")  # userStatus: 1-normal, 2-banned, 3-deleted
    avatar = models.ImageField(upload_to="images/avatars/", null=True, blank=True, default="/", max_length=255)  # avatar

    def toDict(self):  # return as dict
        return {
            "userId": self.userId,
            "username": self.username,
            "email": self.email,
            "gender": self.gender,
            "createTime": self.createTime.strftime("%Y-%m-%d %H:%M:%S"),
            "selfIntroduction": self.selfIntroduction,
            "userStatus": self.userStatus,
            "avatar": self.avatar.url if self.avatar else "",
        }

    class Meta:
        db_table = "user_info"  # table name


# User likes
class UserLikes(models.Model):
    likeId = models.AutoField(primary_key=True, verbose_name="likeId")  # likeId
    userBeenLikedId = models.CharField(max_length=200, verbose_name="userBeenLikedId", default=None)  # userBeenLikedId
    userLikesId = models.CharField(max_length=200, verbose_name="userLikesId", default=None)  # userLikesId
    blogId = models.CharField(max_length=200, verbose_name="blogId", default=None)  # blogId
    createTime = models.DateTimeField(default=datetime.now)  # createTime

    def toDict(self):  # return as dict
        return {
            "likeId": self.likeId,
            "userBeenLikedId": self.userBeenLikedId,
            "userLikesId": self.userLikesId,
            "blogId": self.blogId,
            "createTime": self.createTime.strftime("%Y-%m-%d %H:%M:%S"),
        }

    class Meta:
        db_table = "user_likes"  # table name


# User Follows
class UserFollows(models.Model):
    followId = models.AutoField(primary_key=True, verbose_name="followId")  # followId
    userFollowsId = models.CharField(max_length=200, verbose_name="userFollowsId", default=None)  # userFollowsId
    userBeenFollowedId = models.CharField(max_length=200, verbose_name="userBeenFollowedId", default=None)  # userBeenFollowedId
    createTime = models.DateTimeField(default=datetime.now)  # createTime

    def toDict(self):  # return as dict
        return {
            "followId": self.followId,
            "userFollowsId": self.userFollowsId,
            "userBeenFollowedId": self.userBeenFollowedId,
            "createTime": self.createTime.strftime("%Y-%m-%d %H:%M:%S"),
        }

    class Meta:
        db_table = "user_follows"  # table name


# User login token
class UserLogin(models.Model):
    loginId = models.AutoField(primary_key=True, verbose_name="loginId")  # loginId
    userId = models.CharField(max_length=200, verbose_name="userId", default=None)  # userId
    token = models.CharField(max_length=200, verbose_name="token", default=None)  # token
    createTime = models.DateTimeField(default=datetime.now)  # createTime
    expireTime = models.DurationField(default=timedelta(days=2))  # expireTime, default for 2 days

    def toDict(self):  # return as dict
        return {
            "loginId": self.loginId,
            "userId": self.userId,
            "token": self.token,
            "createTime": self.createTime.strftime("%Y-%m-%d %H:%M:%S"),
            "expireTime": str(self.expireTime),
        }

    class Meta:
        db_table = "user_login"  # table name

    # Check if the token has expired
    def is_expired(self):
        """Check if the token has expired"""
        return timezone.now() > self.createTime + self.expireTime

    # Delete the record if the token has expired
    def delete_if_expired(self):
        """Delete the record if the token has expired"""
        if self.is_expired():
            self.delete()

    @staticmethod
    def check_and_delete_expired_tokens():
        """Check and delete expired tokens"""
        for token in UserLogin.objects.all():
            token.delete_if_expired()
