# import models and serializers
from models.models import models_user
from models.models import models_blog
from api.utils.serializers import user_infomation_ser
from django.core import serializers

# Rest Framework Views
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet

# Authentication, throttling, permissions
from api.utils.throttle import VisitThrottle
from api.utils.permission import BasicUser
from django.contrib import admin
from django.contrib.auth.models import User

from api.utils.auth import Authentication

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

# import other modules
import os
from django.conf import settings
import uuid


# Upload images
class UploadImgaesView(APIView): 

    def url_to_md(image_name, url):
        return f"![{image_name}]({url})"

    def post(self, request, *args, **kwargs):
        try:
            return_value = {"code": 200, "status": None}
            
            images = []
            for key in request.FILES: # May be multiple images
                file_data = request.FILES.get(key)
                image_data = file_data.read()
                image_type = file_data.content_type.split('/')[1]
                # Get the path of the image to be saved
                image_path = os.path.join(settings.BASE_DIR, 'static/images/blogs')
                image_name = f'image_{uuid.uuid4().hex}.{image_type}'
                file_path = os.path.join(image_path, image_name)
                
                # Save the image
                with open(file_path, 'wb') as f:
                    f.write(image_data)
                
                # return image url
                image_url = f'https://bk.petopia.top/static/images/blogs/{image_name}'
                image_md_name = UploadImgaesView.url_to_md(image_name, image_url)
                images.append(image_md_name)
            
            # Return image url
            return_value['data'] = images
            return_value['status'] = "success"
            return_value['code'] = 200

            return JsonResponse(return_value)
        except Exception as e:
            print(e)

# Public blog
class BlogPublishView(APIView):
    authentication_classes = [Authentication,]

    def post(self, request, *args, **kwargs):
        return_value = {"code": None, "msg": None, "data": None}

        # Get user id from request
        user_id = json.loads(request.body).get("userId")  # current user id
        title = json.loads(request.body).get("title")  # blog title
        content = json.loads(request.body).get("content")  # blog content in markdown format
        status = json.loads(request.body).get("status")  # status: 1-published, 2-draft
        tag = json.loads(request.body).get("tag")  # tag

        if int(status) > 2 or int(status) < 1:
            return_value["code"] = 400
            return_value["msg"] = "Invalid status"
            return_value["data"] = {}
            return JsonResponse(return_value)
        elif status is None:
            status = 2  # default status: draft
        try:
            # Check whether the user exists
            user_info = models_user.UserInfo.objects.filter(userId=user_id, userStatus=1).first()

            if user_info is None:
                return_value["code"] = 401  # 401: user not found
                return_value["msg"] = "User not found"
                return_value["data"] = {}
            else:
                # Save new blog
                blog = models_blog.BlogDetails.objects.create(
                    userId=user_id,
                    title=title,
                    content=content,
                    status=status,
                    tag=tag,
                )
                
                # should create image_urls
                image_urls_check = models_blog.BlogImages.objects.filter(blogId=blog.blogId)
                image_list = []
                if image_urls_check.exists():
                    for image in image_urls_check:
                        image_list.append(image.imageUrls)

                data = {
                    "blogId": blog.blogId,
                    "userId": blog.userId,
                    "title": blog.title,
                    "content": blog.content,
                    "imageUr": image_list,
                    "createTime": blog.createTime.strftime("%Y-%m-%d %H:%M:%S"),
                    "modifyTime": blog.modifyTime.strftime("%Y-%m-%d %H:%M:%S"),
                    "publishTime": blog.publishTime.strftime("%Y-%m-%d %H:%M:%S"),
                    "modifyPersonId": blog.modifyPersonId,
                    "status": blog.status,
                    "tag": blog.tag,
                }

                # Return blog info
                return_value["code"] = 200
                return_value["msg"] = "Blog published"
                return_value["data"] = data

        except Exception as e:
            return_value["code"] = 413
            return_value["msg"] = "Error"
            print(e)

        return JsonResponse(return_value)

# Search blog details by blog id
class SearchBlogByIdView(APIView):
    
    def post(self, request, *args, **kwargs):
        return_value = {"code": None, "msg": None, "data": None}
        blog_id = json.loads(request.body).get("blogId")  # current blogId
        
        try:
            # Get blog details by blog_id
            blog_check = models_blog.BlogDetails.objects.filter(blogId=blog_id)
            if blog_check.exists():
                blog = blog_check.values("blogId", "userId", "tag", "title", "content", "createTime", "modifyTime", "modifyPersonId", "publishTime").first()

                # Add Images
                blog_images_check = models_blog.BlogImages.objects.filter(blogId=blog_id)
                blog_images = []
                if blog_images_check.exists():
                    blog_images = list(blog_images_check.values_list("imageUrls"))[0][0]

                # Add Avatar
                avatar = models_user.UserInfo.objects.filter(userId=blog["userId"]).values("avatar").first()

                # Add to blog dict
                blog["avatar"] = avatar['avatar']
                blog["imageUrl"] = blog_images

                # Return data
                return_value["code"] = 200
                return_value["msg"] = "Blog found"
                return_value["data"] = blog
            else:
                return_value["code"] = 201
                return_value["msg"] = "Blog not found"
                return_value["data"] = {}
        except Exception as e:
            return_value["code"] = 413
            return_value["msg"] = "Error"

        return JsonResponse(return_value)

# Blogs list
class BlogsView(APIView):
    # authentication_classes = [Authentication,]

    def post(self, request, *args, **kwargs):
        return_value = {"code": None, "msg": None, "data": None}

        # Get user id from request
        user_id = json.loads(request.body).get("userId")  # current user id
        if user_id == "":
            user_id = 0
        try:
            # Get all blog details
            blog_check = models_blog.BlogDetails.objects
            if blog_check.exists():
                blog_details = blog_check.values("blogId", "userId", "tag", "title", "content", "createTime", "modifyTime", "modifyPersonId", "publishTime").order_by("-publishTime")
                # Add isEditable to each blog
                blog_list = []
                for blog in blog_details:
                    # Check if user has editing permissions
                    isEditable = 0
                    if int(user_id) > 0:
                        if int(user_id) == int(blog["userId"]) or User.objects.get(id=user_id).is_staff:
                            isEditable = 1
                    

                    # Add Images
                    blog_id = blog["blogId"]
                    blog_images_check = models_blog.BlogImages.objects.filter(blogId=blog_id)
                    blog_images = []
                    if blog_images_check.exists():
                        blog_images = list(blog_images_check.values_list("imageUrls"))[0][0]
                        
                    # Add Avatar
                    avatar = models_user.UserInfo.objects.filter(userId=blog["userId"]).values("avatar").first()

                    # Check if user has liked the blog
                    isLiked = 0
                    if models_user.UserLikes.objects.filter(userLikesId=user_id, blogId=blog["blogId"]).exists():
                        isLiked = 1
                        
                    # check wehther user has authority to edit
                    isEditable = 0 # 0-does not have authority, 1-has authority
                    if int(user_id) > 0:
                        if user_id == blog["userId"] or User.objects.get(id=user_id).is_staff:
                            isEditable = 1
                    
                    # Add to blog dict
                    blog["isEditable"] = isEditable
                    blog["isLiked"] = isLiked
                    blog["avatar"] = avatar['avatar']
                    blog["imageUrl"] = blog_images
                    blog_list.append(blog)

                # Return data
                return_value["code"] = 200
                return_value["msg"] = "Blogs found"
                return_value["data"] = {
                    "blogs": blog_list,
                }
            else:
                return_value["code"] = 201
                return_value["msg"] = "No blogs found"
                return_value["data"] = {}
        except Exception as e:
            return_value["code"] = 413
            return_value["msg"] = "Error"
            print(e)

        return JsonResponse(return_value)


# Blog edit
class BlogEditView(APIView):
    # authentication_classes = [Authentication,]

    def post(self, request, *args, **kwargs):
        return_value = {"code": None, "msg": None, "data": None}

        # Get blog id from request
        blog_id = json.loads(request.body).get("blogId")
        current_user_id = json.loads(request.body).get("currentUserId")
        blog_title = json.loads(request.body).get("blogTitle")
        blog_content = json.loads(request.body).get("blogContent")
        blog_status = json.loads(request.body).get("blogStatus")
        tag = json.loads(request.body).get("tag")

        try:
            check_user = User.objects.filter(id=current_user_id)
            if check_user.exists():
                # Check whether the blog exists
                blog = models_blog.BlogDetails.objects.filter(blogId=blog_id).first()
                # Check if the blog exists
                if blog is None:  # 401: blog not found
                    return_value["code"] = 402
                    return_value["msg"] = "Blog not found"
                    return_value["data"] = {}
                else:
                    # Get user info
                    user_id = blog.userId
                    user_info = models_user.UserInfo.objects.filter(userId=user_id, userStatus=1).first()

                    # Check if the user has permission to edit the blog
                    if int(current_user_id) == int(user_id) or User.objects.get(id=current_user_id).is_staff:
                        # Update blog information
                        if blog_title:
                            blog.title = blog_title
                        if blog_content:
                            blog.content = blog_content
                        if blog_status:
                            blog.status = blog_status
                        if tag:
                            blog.tag = tag
                        blog.modifyTime = datetime.now()
                        blog.modifyPersonId = current_user_id
                        blog.save()

                        # Return updated blog information
                        return_value["code"] = 200
                        return_value["msg"] = "Blog updated successfully"
                        return_value["data"] = {
                            "blogId": blog.blogId,
                            "userId": blog.userId,
                            "blogTitle": blog.title,
                            "blogTag": blog.tag,
                            "blogContent": blog.content,
                            "blogStatus": blog.status,
                            "createTime": blog.createTime.strftime("%Y-%m-%d %H:%M:%S"),
                            "modifyTime": blog.modifyTime.strftime("%Y-%m-%d %H:%M:%S"),
                            "publishTime": blog.publishTime.strftime("%Y-%m-%d %H:%M:%S") if blog.publishTime else None,
                            "modifyPersonId": blog.modifyPersonId,
                            "username": user_info.username,
                            "avatar": user_info.avatar.url if user_info.avatar else "",
                        }
                    else:
                        return_value["code"] = 403  # 403: no permission to edit the blog
                        return_value["msg"] = "This user does not have permission to edit the blog"
                        return_value["data"] = {}
            else:
                return_value["code"] = 401
                return_value["msg"] = "User not found"
                return_value["data"] = {}
        except Exception as e:
            return_value["code"] = 413
            return_value["msg"] = "Error"
            print(e)

        return JsonResponse(return_value)


# Blog like
class BlogLikeView(APIView):
    authentication_classes = [Authentication,]

    def post(self, request, *args, **kwargs):
        return_value = {"code": None, "msg": None, "data": None}

        # Get user info from request
        userLikesId = json.loads(request.body).get("userId")  # user who is liking
        blogId = json.loads(request.body).get("blogId")  # blog being liked

        try:
            # Check whether the users exist
            user_check = models_user.UserInfo.objects.filter(userId=userLikesId, userStatus=1).first()
            blog_check = models_blog.BlogDetails.objects.filter(blogId=blogId).first()
            if not user_check:  # 401: user not found
                return_value["code"] = 401
                return_value["msg"] = "User not found"
                return_value["data"] = {}
            elif not blog_check:  # 402: blog not found
                return_value["code"] = 402
                return_value["msg"] = "Blog not found"
                return_value["data"] = {}
            else:  # both user and blog exist
                user_been_like_check = models_user.UserInfo.objects.filter(userId=blog_check.userId, userStatus=1).first()
                user_been_like_id = user_been_like_check.userId
                check_like_status = models_user.UserLikes.objects.filter(userLikesId=userLikesId, userBeenLikedId=user_been_like_id, blogId=blogId)
                if check_like_status.exists():
                    return_value["code"] = 403  # 403: user has already liked this blog
                    return_value["msg"] = "User has already liked this blog"
                    return_value["data"] = {}
                else:
                    # Create user like record
                    models_user.UserLikes.objects.create(userLikesId=userLikesId, userBeenLikedId=user_been_like_id, blogId=blogId)
                    data = {"userId": userLikesId, "blogId": blogId}
                    # return success message
                    return_value["code"] = 200
                    return_value["msg"] = "Blog liked successfully"
                    return_value["data"] = data

        except Exception as e:
            print("e", e)
            return_value["code"] = 413
            return_value["msg"] = "Error"
            print(e)

        return JsonResponse(return_value)


# Blog like check
class BlogLikeCheckView(APIView):
    authentication_classes = [Authentication,]

    def post(self, request, *args, **kwargs):
        return_value = {"code": None, "msg": None, "data": None}

        # Get user info from request
        userLikesId = json.loads(request.body).get("userId")  # user who is liking
        blogId = json.loads(request.body).get("blogId")  # blog being liked

        try:
            # Check whether the users exist
            user_check = models_user.UserInfo.objects.filter(userId=userLikesId, userStatus=1).first()
            blog_check = models_blog.BlogDetails.objects.filter(blogId=blogId).first()
            if not user_check:  # 401: user not found
                return_value["code"] = 401
                return_value["msg"] = "User not found"
                return_value["data"] = {}
            elif not blog_check:  # 402: blog not found
                return_value["code"] = 402
                return_value["msg"] = "Blog not found"
                return_value["data"] = {}
            else:  # both user and blog exist
                user_been_like_check = models_user.UserInfo.objects.filter(userId=blog_check.userId, userStatus=1).first()
                user_been_like_id = user_been_like_check.userId
                check_like_status = models_user.UserLikes.objects.filter(userLikesId=userLikesId, userBeenLikedId=user_been_like_id, blogId=blogId)
                data = {"userId": userLikesId, "blogId": blogId}

                if check_like_status.exists():
                    data["likeStatus"] = True
                    return_value["code"] = 200  # 403: user has already liked this blog
                    return_value["msg"] = "User has already liked this blog"
                    return_value["data"] = data
                else:
                    # Create user like record
                    # return success message
                    data["likeStatus"] = False
                    return_value["code"] = 201
                    return_value["msg"] = "User haven't like this blog"
                    return_value["data"] = data

        except Exception as e:
            return_value["code"] = 413
            return_value["msg"] = "Error"
            print(e)

        return JsonResponse(return_value)


# Blog unlike
class BlogUnlikeView(APIView):
    authentication_classes = [Authentication,]

    def post(self, request, *args, **kwargs):
        return_value = {"code": None, "msg": None, "data": None}

        # Get user info from request
        userLikesId = json.loads(request.body).get("userId")  # user who is unliking
        blogId = json.loads(request.body).get("blogId")  # blog being unliked

        try:
            # Check whether the users exist
            user_check = models_user.UserInfo.objects.filter(userId=userLikesId, userStatus=1).first()
            blog_check = models_blog.BlogDetails.objects.filter(blogId=blogId).first()
            if not user_check:  # 401: user not found
                return_value["code"] = 401
                return_value["msg"] = "User not found"
                return_value["data"] = {}
            elif not blog_check:  # 402: blog not found
                return_value["code"] = 402
                return_value["msg"] = "Blog not found"
                return_value["data"] = {}
            else:  # both user and blog exist
                check_like_status = models_user.UserLikes.objects.filter(userLikesId=userLikesId, blogId=blogId)
                if not check_like_status.exists():
                    return_value["code"] = 403  # 403: user has not liked this blog
                    return_value["msg"] = "User has not liked this blog"
                    return_value["data"] = {}
                else:
                    # Delete user like record
                    check_like_status.delete()
                    data = {"userId": userLikesId, "blogId": blogId}
                    # return success message
                    return_value["code"] = 200
                    return_value["msg"] = "Blog unliked successfully"
                    return_value["data"] = data

        except Exception as e:
            return_value["code"] = 413
            return_value["msg"] = "Error"
            print(e)

        return JsonResponse(return_value)


# Search blog
class SearchBlogByKeywordsView(APIView):
    # authentication_classes = [Authentication,]

    def post(self, request, *args, **kwargs):
        return_value = {"code": None, "msg": None, "data": None}

        # Get search keyword from request
        search_keyword = json.loads(request.body).get("searchKeyword")

        try:
            # Search blog
            blogs_search = models_blog.BlogDetails.objects.filter(Q(title__contains=search_keyword) | Q(content__contains=search_keyword))
            blog_list = []

            # Check if search result exists
            if blogs_search.exists():
                blogs = blogs_search.order_by("-publishTime")

                # convert blog object to dict
                for blog in blogs:
                    blog_dict = blog.toDict()
                    blog_list.append(blog_dict)

                # return success message
                return_value["code"] = 200
                return_value["msg"] = "Search successful"

            else:
                return_value["code"] = 201
                return_value["msg"] = "No blogs found"

            # return search result
            return_value["data"] = blog_list

        except Exception as e:
            return_value["code"] = 413
            return_value["msg"] = "Error"
            print(e)

        return JsonResponse(return_value)


# Delete blog
class DeleteBlogView(APIView):
    authentication_classes = [Authentication,]

    def post(self, request, *args, **kwargs):
        return_value = {"code": None, "msg": None, "data": None}

        # Get blogId from request
        blogId = json.loads(request.body).get("blogId")
        current_user_id = json.loads(request.body).get("userId")

        try:
            # check user exists
            user_check = models_user.UserInfo.objects.filter(userId=current_user_id, userStatus=1)
            if user_check.exists():
                # Check whether the blog exists
                blog_check = models_blog.BlogDetails.objects.filter(blogId=blogId)
                print("blog", blog_check)
                if blog_check.exists():  # 402: blog not found
                    userId = list(blog_check.values_list("userId", flat=True))[0]
                    if int(userId) == int(current_user_id) or User.objects.get(id=current_user_id).is_superuser:
                        # Delete blog record
                        blog_check.delete()
                        # return success message
                        return_value["code"] = 200
                        return_value["msg"] = "Blog deleted successfully"
                        return_value["data"] = {"blogId": blogId, "userId": userId}
                    else:
                        return_value["code"] = 403
                        return_value["msg"] = "This user has no authority to the blog"
                        return_value["data"] = {}

                else:  # blog exists
                    # check if the user has access of the blog
                    return_value["code"] = 402
                    return_value["msg"] = "Blog not found"
                    return_value["data"] = {}
            else:
                return_value["code"] = 401
                return_value["msg"] = "User not found"
                return_value["data"] = {}
        except Exception as e:
            return_value["code"] = 413
            return_value["msg"] = "Error"
            print(e)

        return JsonResponse(return_value)

# User profile view
class UserProfileListView(ModelViewSet):  
    # authentication_classes = [
    #     Authentication,
    # ]
    queryset = models_user.UserInfo.objects.all()
    serializer_class = user_infomation_ser.UserInfoSer
