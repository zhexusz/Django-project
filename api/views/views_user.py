# import models and serializers
from models.models import models_user
from models.models import models_blog
from api.utils.serializers import user_infomation_ser
from django.core import serializers
from django.db.models import Count

# Rest Framework Views
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet

# Authentication, throttling, permissions
from api.utils.throttle import VisitThrottle
from api.utils.permission import BasicUser
from django.contrib import admin
from django.contrib.auth.models import User
from api.utils.auth import Authentication

# from api.utils.auth import Authentication

# data process
import json
from django.forms import model_to_dict
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.utils import timezone as datetime
from django.db.models import Q
from django.utils.timezone import now, timedelta

# Other functional components of rest framework (return formatting, version control, etc.)
from rest_framework.response import Response
from rest_framework.versioning import BaseVersioning, QueryParameterVersioning, URLPathVersioning
from django.contrib.auth import authenticate




# User Login
class UserLoginAuthView(APIView):
    def md5(user):
        import hashlib
        import time

        ctime = str(time.time())

        m = hashlib.md5(bytes(user, encoding="utf-8"))
        m.update(bytes(ctime, encoding="utf-8"))
        return m.hexdigest()

    def post(self, request, *args, **kwargs):
        return_value = {"code": None, "msg": None, "data": None}  # Create a return value dictionary
        username = json.loads(request.body).get("username")
        password = json.loads(request.body).get("password")
        print("login:", username, password)

        try:
            # using django auth
            user = authenticate(username=username, password=password)
            print("hi")
            if not user:
                return_value["code"] = 401  # User not found or password incorrect
                return_value["msg"] = "Username or password incorrect!"
                return_value["data"] = {}
                print("not user, username is:", username, "password is:", password)
            else:
                # Get user_id
                userId = models_user.UserInfo.objects.filter(username=username).values("userId").first()
                userId = list(userId.values())[0]

                # Create token and update token
                print("222, userId is:", userId)
                token = UserLoginAuthView.md5(username)
                models_user.UserLogin.objects.update_or_create(defaults={"token": token}, userId=userId)
                data = {"token": token, "user_id": userId, "access": "admin", "name": username}
                return_value["code"] = 200
                return_value["msg"] = "Login Success!"
                return_value["data"] = data

        except Exception as e:
            return_value["code"] = 503
            return_value["msg"] = "Error"

        return JsonResponse(return_value)


# User Logout
class UserLogoutView(APIView):
    # authentication_classes = [
    # Authentication,
    # ]

    def post(self, request, *args, **kwargs):
        return_value = {"code": None, "status": None, "data": None}
        user_id = json.loads(request.body).get("userId")

        if user_id is None:
            return_value["code"] = 412
            return_value["status"] = "Please use token or user id to logout!"
            return_value["data"] = {}
            return JsonResponse(return_value)
        try:
            # Check wehther token exists

            check_token = models_user.UserLogin.objects.filter(userId=user_id)
            if check_token.exists():
                # Delete token
                check_token.delete()
                return_value["code"] = 200
                return_value["status"] = "Logout successfully!"
                return_value["data"] = {}

            else:
                return_value["code"] = 401
                return_value["status"] = "Token does not exist, or user is already logout!"
                return_value["data"] = {}

        except Exception as e:
            return_value["code"] = 413
            return_value["status"] = "Error"
            return_value["data"] = e
            print(e)
        return JsonResponse(return_value)


# Create User / Register
class UserCreateView(APIView):
    # authentication_classes = [
    #     Authentication,
    # ]

    def post(self, request, *args, **kwargs):
        return_value = {"code": None, "msg": None, "data": None}
        username = json.loads(request.body).get("username")
        password = json.loads(request.body).get("password")
        email = json.loads(request.body).get("email")
        createTime = datetime.now()
        check_user = User.objects.filter(username=username).exists()

        try:
            if username is None or password is None:
                return_value["code"] = 401
                return_value["msg"] = "Please enter username and password!"
                return_value["data"] = {}

            elif username is not None:
                if check_user is True:
                    return_value["code"] = 402
                    return_value["msg"] = "Error, user already exists!"
                    return_value["data"] = {}

                if check_user is False:
                    # Create Auth User
                    User.objects.create_user(username=username, password=password, email=email)

                    # Check whether the user has been created
                    authcheck = User.objects.filter(username=username, email=email).first()

                    # Get user_id
                    userId = authcheck.id
                    
                    # Create default avatar
                    avatar = "https://bk.petopia.top/static/images/users/user_avatar_female.png"

                    # Create user information
                    models_user.UserInfo.objects.create(userId=userId, username=username, email=email, createTime=createTime, avatar=avatar)

                    return_value["code"] = 200
                    return_value["data"] = {"username": username, "userId": userId}
                    return_value["msg"] = "Create successfully!"

        except Exception as e:
            return_value["code"] = 403
            print(e)
        return JsonResponse(return_value)


# Delete User / Delete Account
class UserDeleteView(APIView):
    # authentication_classes = [
    #     Authentication,
    # ]

    def post(self, request, *args, **kwargs):
        data = {"userId": None, "username": None}
        return_value = {"code": None, "status": None, "data": data}
        user_id = json.loads(request.body).get("userId")

        if user_id is None:
            return_value["code"] = 412
            return_value["status"] = "Please enter user id"
            return JsonResponse(return_value)
        try:
            # Check whether the user exists
            check_user = User.objects.filter(id=user_id).exists()
            if check_user is False:
                return_value["code"] = 401
                return_value["status"] = "User does not exist"
                return JsonResponse(return_value)

            # Update user status
            User.objects.filter(id=user_id).update(is_active=0)  # 0-inactive, 1-active, for auth_user
            models_user.UserInfo.objects.filter(userId=user_id, userStatus=1).update(userStatus=3)  # 1-active, 2- inactive, 3- deleted, for user_info

            # Get username for return
            get_username = models_user.UserInfo.objects.filter(userId=user_id, userStatus=1)
            username = list(get_username.values_list("username"))[0][0]

            # Return data
            data["userId"] = user_id
            data["username"] = username
            return_value["code"] = 200
            return_value["status"] = "User deleted successfully"
            return_value["data"] = data
        except Exception as e:
            return_value["code"] = 413
            return_value["status"] = "Error"
            print(e)
        return JsonResponse(return_value)


# Change Password
class UserChangePasswordView(APIView):
    # authentication_classes = [
    #     Authentication, 
    # ]

    def post(self, request, *args, **kwargs):
        return_value = {"code": None, "msg": None, "data": None}
        user_id = json.loads(request.body).get("userId")
        old_password = json.loads(request.body).get("oldPassword")
        new_password = json.loads(request.body).get("newPassword")

        try:
            # Check whether the user exists
            check_user = User.objects.filter(id=user_id).exists()
            if check_user is False:
                return_value["code"] = 401
                return_value["msg"] = "User does not exist"
                return_value["data"] = {}
            else:
                # Check if old password is correct
                user = User.objects.get(id=user_id)
                if not user.check_password(old_password):
                    return_value["code"] = 402
                    return_value["msg"] = "Old password is incorrect"
                    return_value["data"] = {}
                else:
                    # Change password
                    user.set_password(new_password)
                    user.save()

                    return_value["code"] = 200
                    return_value["msg"] = "Password changed successfully"
                    return_value["data"] = {"userId": user_id, "username": user.username}
        except Exception as e:
            return_value["code"] = 413
            return_value["msg"] = "Error"
            print(e)
        return JsonResponse(return_value)


# User Info Edit
class UserInfoEditView(APIView):
    # authentication_classes = [Authentication,]

    def post(self, request, *args, **kwargs):
        return_value = {"code": None, "msg": None, "data": None}

        # Get user info from request
        user_id = json.loads(request.body).get("userId")
        username = json.loads(request.body).get("username")
        email = json.loads(request.body).get("email")
        gender = json.loads(request.body).get("gender")
        self_introduction = json.loads(request.body).get("selfIntroduction")

        try:
            # Check whether the user exists
            user = models_user.UserInfo.objects.filter(userId=user_id, userStatus=1).first()
            if not user:  # user does not exist
                return_value["code"] = 401  # 401: user not found
                return_value["msg"] = "User not found"
                return_value["data"] = {}
            else:  # user exists
                # Update user info in django user_info
                user.username = username
                user.email = email
                user.gender = gender
                user.selfIntroduction = self_introduction
                user.save()

                # Update user info in auth_user
                user_check = User.objects.filter(id=user_id)
                if user_check.exists():
                    user_check = user_check.first()
                    user_check.username = username
                    user_check.email = email
                    user_check.save()

                # return user info
                return_value["code"] = 200
                return_value["msg"] = "User information updated successfully"
                return_value["data"] = user.toDict()

        except Exception as e:
            return_value["code"] = 413
            return_value["msg"] = "Error"
            return_value["data"] = e
            print(e)

        return JsonResponse(return_value)


# Get Current User Info
class CurrentUserView(APIView):
    # authentication_classes = [Authentication,]

    def post(self, request, *args, **kwargs):
        return_value = {"code": None, "msg": None, "data": None}

        # Get user info from request
        user_id = json.loads(request.body).get("userId")

        try:
            # Check whether the user exists
            user = models_user.UserInfo.objects.filter(userId=user_id, userStatus=1).first()
            if not user:  # user does not exist
                return_value["code"] = 401  # 401: user not found
                return_value["msg"] = "User not found"
                return_value["data"] = {}
            else:  # user exists
                # Update user info
                userId = user.userId
                username = user.username
                gender = user.gender
                # avatar = user.avatar.url
                data = {"userId": userId, "username": username, "gender": gender, "avatar": ""}

                # return user info
                return_value["code"] = 200
                return_value["msg"] = "Success"
                return_value["data"] = data

        except Exception as e:
            return_value["code"] = 413
            return_value["msg"] = "Error"
            print(e)

        return JsonResponse(return_value)


# User Follow
class UserFollowView(APIView):
    authentication_classes = [Authentication,]

    def post(self, request, *args, **kwargs):
        return_value = {"code": None, "msg": None, "data": None}

        # Get user info from request
        userFollowId = json.loads(request.body).get("userFollowId")  # user who is following
        userBeenFollowedId = json.loads(request.body).get("userBeenFollowedId")  # user who is being followed

        try:
            # Check whether the users exist
            user_follow_check = models_user.UserInfo.objects.filter(userId=userFollowId, userStatus=1).first()
            user_followed_check = models_user.UserInfo.objects.filter(userId=userBeenFollowedId, userStatus=1).first()
            if not user_follow_check or not user_followed_check:  # user does not exist
                return_value["code"] = 401  # 401: user not found
                return_value["msg"] = "User not found"
                return_value["data"] = {}
            elif userFollowId == userBeenFollowedId:
                return_value["code"] = 402  # 402: user can't follow self
                return_value["msg"] = "Can't follow self"
                return_value["data"] = {}
            else:  # both users exist
                check_follow_status = models_user.UserFollows.objects.filter(userFollowsId=userFollowId, userBeenFollowedId=userBeenFollowedId)
                if check_follow_status.exists():
                    return_value["code"] = 403  # 400: user has already followed this user
                    return_value["msg"] = "User has already followed this user"
                    return_value["data"] = {}
                else:
                    # Add user follow record
                    models_user.UserFollows.objects.create(userFollowsId=userFollowId, userBeenFollowedId=userBeenFollowedId)
                    # return success message
                    return_value["code"] = 200
                    return_value["msg"] = "User followed successfully"
                    return_value["data"] = {"userFollowsId": userFollowId, "userBeenFollowedId": userBeenFollowedId}

        except Exception as e:
            return_value["code"] = 413
            return_value["msg"] = "Error"
            print(e)

        return JsonResponse(return_value)


# User Unfollow
class UserUnfollowView(APIView):
    authentication_classes = [Authentication,]

    def post(self, request, *args, **kwargs):
        return_value = {"code": None, "msg": None, "data": None}

        # Get user info from request
        userFollowId = json.loads(request.body).get("userFollowId")  # user who is following
        userBeenFollowedId = json.loads(request.body).get("userBeenFollowedId")  # user who is being followed

        try:
            # Check whether the users exist
            user_follow_check = models_user.UserInfo.objects.filter(userId=userFollowId, userStatus=1).first()
            user_followed_check = models_user.UserInfo.objects.filter(userId=userBeenFollowedId, userStatus=1).first()
            if not user_follow_check or not user_followed_check:  # user does not exist
                return_value["code"] = 401  # 401: user not found
                return_value["msg"] = "User not found"
                return_value["data"] = {}
            elif userFollowId == userBeenFollowedId:
                return_value["code"] = 402  # 402: user can't follow/unfollow self
                return_value["msg"] = "Can't follow/unfollow self"
                return_value["data"] = {}
            else:  # both users exist
                check_follow_status = models_user.UserFollows.objects.filter(userFollowsId=userFollowId, userBeenFollowedId=userBeenFollowedId)
                if not check_follow_status.exists():
                    return_value["code"] = 403  # 403: user has not followed this user
                    return_value["msg"] = "User has not followed this user"
                    return_value["data"] = {}
                else:
                    # Delete user follow record
                    check_follow_status.delete()
                    # return success message
                    return_value["code"] = 200
                    return_value["msg"] = "User unfollowed successfully"
                    return_value["data"] = {"userFollowsId": userFollowId, "userBeenFollowedId": userBeenFollowedId}

        except Exception as e:
            return_value["code"] = 413
            return_value["msg"] = "Error"
            print(e)

        return JsonResponse(return_value)


# User Profile
class UserProfileView(APIView):
    # authentication_classes = [Authentication,]
    def post(self, request, *args, **kwargs):
        return_value = {"code": None, "msg": None, "data": None}

        # Get user id from request
        user_id = json.loads(request.body).get("userId")  # current user id
        user_profile_id = json.loads(request.body).get("userProfileId")  # whose profile is being viewed

        if user_id == "":
            user_id = 0
        print("userId", user_id)
        try:
            # Check whether the user exists
            user_info = models_user.UserInfo.objects.filter(userId=user_id, userStatus=1).first()
            user_profile_info = models_user.UserInfo.objects.filter(userId=user_profile_id, userStatus=1).first()

            # Check whether both users exist
            if user_info is None or user_profile_info is None:
                return_value["code"] = 401  # 401: user not found
                return_value["msg"] = "User not found"
                return_value["data"] = {}
            else:
                # Get user profile data
                user_profile = {
                    "userId": user_profile_info.userId,
                    "username": user_profile_info.username,
                    "avatar": user_profile_info.avatar.url if user_profile_info.avatar else "",
                }
                avatar_url = user_profile['avatar'].replace("/static/images/https%3A/", "").replace("%0D", "")
                avatar_url = "https://" + avatar_url
                print("original: ", user_profile['avatar'])
                user_profile['avatar'] = avatar_url
                print("hi", user_profile['avatar'])

                # Get user likes
                likes_count = models_user.UserLikes.objects.filter(userLikesId=user_profile_id).count()
                been_liked_count = models_user.UserLikes.objects.filter(userBeenLikedId=user_profile_id).count()

                # Get user follows
                follows_count = models_user.UserFollows.objects.filter(userFollowsId=user_profile_id).count()
                been_followed_count = models_user.UserFollows.objects.filter(userBeenFollowedId=user_profile_id).count()

                # Get user blogs
                user_blogs = models_blog.BlogDetails.objects.filter(userId=user_profile_id).values("blogId", "userId", "tag", "title", "content", "createTime", "modifyTime", "modifyPersonId", "publishTime")
                
                # Get isEditable
                isEditable = 0
                if user_id == user_profile_id or User.objects.get(id=user_id).is_staff:
                    isEditable = 1
                
                # Add isFollowed
                isFollowed = 0 # 0-not followed, 1-followed, 2-self
                if user_id == user_profile_id:
                    isFollowed = 2
                else:
                    followed_check = models_user.UserFollows.objects.filter(userFollowsId=user_id, userBeenFollowedId=user_profile_id)
                    if followed_check.exists():
                        isFollowed = 1
                
                # Add isEditable to each blog
                blog_list = []
                for blog in user_blogs:

                    # Add Images
                    blog_id = blog["blogId"]
                    userId = blog["userId"]
                    title = blog["title"]
                    tag = blog["tag"]
                    content = blog["content"]
                    createTime = blog["createTime"]
                    modifyTime = blog["modifyTime"]
                    modifyPersonId = blog["modifyPersonId"]
                    publishTime = blog["publishTime"]
                    blog_images_check = models_blog.BlogImages.objects.filter(blogId=blog_id)
                    blog_images = []
                    if blog_images_check.exists():
                        blog_images = list(blog_images_check.values_list("imageUrls"))[0][0]
                    
                    # Add isLiked
                    isLiked = 0
                    liked_check = models_user.UserLikes.objects.filter(userLikesId=user_id, userBeenLikedId=userId, blogId=blog_id)
                    if liked_check.exists():
                        isLiked = 1
                    
                    # Add Avatar
                    avatar = models_user.UserInfo.objects.filter(userId=blog["userId"]).values("avatar").first()
                    avatar_new = avatar["avatar"].strip()

                    # check wehther user has authority to edit
                    isEditable = 0 # 0-does not have authority, 1-has authority
                    if user_id == user_profile_id or User.objects.get(id=user_id).is_staff:
                        isEditable = 1
                    
                    blog_details = {
                        "blogId": blog_id,
                        "userId": userId,
                        "title": title,
                        "tag": tag,
                        "content": content,
                        "createTime": createTime,
                        "modifyTime": modifyTime,
                        "modifyPersonId": modifyPersonId,
                        "publishTime": publishTime,
                        "imageUrl": blog_images,
                        "isLiked": isLiked,
                        "avatar": avatar_new,
                        "isEditable": isEditable,
                    }
                    blog_list.append(blog_details)

                # Return data
                return_value["code"] = 200
                return_value["msg"] = "User profile found"
                return_value["data"] = {
                    "userProfile": user_profile,
                    "likes": likes_count,
                    "beenLiked": been_liked_count,
                    "follows": follows_count,
                    "beenFollowed": been_followed_count,
                    # "blogs": list(user_blogs),
                    "blogs": blog_list,
                    "isEditable": isEditable,
                    "isFollowed": isFollowed,
                }

        except Exception as e:
            return_value["code"] = 413
            return_value["msg"] = "Error"
            print(e)

        return JsonResponse(return_value)

# View templates
class UserProfileListView(ModelViewSet):
    # authentication_classes = [
    #     Authentication,
    # ]
    queryset = models_user.UserInfo.objects.all()
    serializer_class = user_infomation_ser.UserInfoSer
