# import models and serializers
from models.models import models_map
from models.models import models_user
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



# add school
class AddSchoolView(APIView):
    def post(self, request, *args, **kwargs):
        return_value = {"code": None, "msg": None, "data": None}

        # Get school info from request
        school_name = json.loads(request.body).get("schoolName")
        latitude = json.loads(request.body).get("latitude")
        longitude = json.loads(request.body).get("longitude")
        course_ids = json.loads(request.body).get("courseIds")

        try:
            # Check if the school already exists
            existing_school = models_map.MapSchoolInfo.objects.filter(schoolName=school_name, schoolStatus=1)
            if existing_school.exists():
                return_value["code"] = 406  # 406: school already exists
                return_value["msg"] = "School already exists"
                return_value["data"] = {}

            else:
                # Create school
                new_school = models_map.MapSchoolInfo.objects.create(schoolName=school_name, latitude=latitude, longitude=longitude)

                # Add courses to the school
                for course_id in course_ids:
                    course = models_map.MapCourseInfo.objects.get(courseId=course_id)
                    models_map.MapSchoolCourseInfo.objects.create(schoolId=new_school, courseId=course)

                # Return created school information
                return_value["code"] = 200
                return_value["msg"] = "School created successfully"
                return_value["data"] = new_school.toDict()

        except Exception as e:
            return_value["code"] = 413
            return_value["msg"] = "Error"
            print(e)

        return JsonResponse(return_value)


class AddCourseView(APIView):
    def post(self, request, *args, **kwargs):
        return_value = {"code": None, "msg": None, "data": None}

        # Get course info from request
        course_title = json.loads(request.body).get("courseTitle")
        course_content = json.loads(request.body).get("courseContent")
        course_image = json.loads(request.body).get("courseImage")
        course_status = json.loads(request.body).get("courseStatus")
        

        try:
            # Create new course
            course = models_map.MapCourseInfo.objects.create(courseTitle=course_title, courseContent=course_content, courseImage=course_image, courseStatus=course_status)
            data = course.toDict()

            # Return course info
            return_value["code"] = 200
            return_value["msg"] = "Course info added"
            return_value["data"] = data

        except Exception as e:
            return_value["code"] = 413
            return_value["msg"] = "Error"
            print(e)

        return JsonResponse(return_value)


class SchoolListView(APIView):
    def post(self, request, *args, **kwargs):
        return_value = {"code": None, "msg": None, "data": None}
        user_id = json.loads(request.body).get("userId")

        try:
            # check user exist
            user_check = models_user.UserInfo.objects.filter(userId=user_id, userStatus=1)
            if user_check.exists():
                school_search = models_map.MapSchoolInfo.objects.all()
                if school_search.exists():
                    data = []
                    for school in school_search:
                        school_dict = school.toDict()
                        userId = user_check[0].userId
                        if User.objects.get(id=userId).is_staff:  # admin user
                            school_dict["isEditable"] = 1
                        else:
                            school_dict["isEditable"] = 2
                        data.append(school_dict)
                    # Return pet info
                    return_value["code"] = 200
                    return_value["msg"] = "Schools info found"
                    return_value["data"] = data
                else:  # schools not found
                    return_value["code"] = 201
                    return_value["msg"] = "Schools not found"
                    return_value["data"] = {}
            else:
                return_value["code"] = 401
                return_value["msg"] = "User not found"
                return_value["data"] = {}
        except Exception as e:
            print(e)
        return JsonResponse(return_value)


class CourseListView(APIView):
    def post(self, request, *args, **kwargs):
        return_value = {"code": None, "msg": None, "data": None}
        school_id = json.loads(request.body).get("schoolId")
        user_id = json.loads(request.body).get("userId")
        try:
            # check user exist
            user_check = models_user.UserInfo.objects.filter(userId=user_id, userStatus=1)
            if user_check.exists():
                school_search = models_map.MapSchoolInfo.objects.filter(schoolId=school_id)
                if school_search.exists():
                    school = school_search.first()
                    data = []
                    for course in school.course.all():
                        course_dict = course.toDict()
                        if User.objects.get(id=user_id).is_staff:  # admin user
                            course_dict["isEditable"] = 1
                        else:
                            course_dict["isEditable"] = 2
                        
                        # Add school location info (for map)
                        course_dict['longitude'] = school.longitude
                        course_dict['latitude'] = school.latitude
                        
                        # delete the /t in the image
                        course_dict["courseImage"] = course.courseImage.rstrip()
                        
                        # add school name
                        course_dict['schoolName'] = school.schoolName


                        data.append(course_dict)
                    # Return course info
                    return_value["code"] = 200
                    return_value["msg"] = "Courses info found"
                    return_value["data"] = data
                else:  # school not found
                    return_value["code"] = 201
                    return_value["msg"] = "School not found"
                    return_value["data"] = {}
            else:
                return_value["code"] = 401
                return_value["msg"] = "User not found"
                return_value["data"] = {}
        except Exception as e:
            print(e)
            return_value["code"] = 413
            return_value["msg"] = "Error"

        return JsonResponse(return_value)


class AddVetView(APIView):
    def post(self, request, *args, **kwargs):
        return_value = {"code": None, "msg": None, "data": None}

        # Get vet info from request
        vet_name = json.loads(request.body).get("vetName")
        latitude = json.loads(request.body).get("latitude")
        longitude = json.loads(request.body).get("longitude")
        address = json.loads(request.body).get("address")
        vetDescription = json.loads(request.body).get("vetDescription")

        try:
            # Check if the vet already exists
            existing_vet = models_map.MapVetInfo.objects.filter(vetName=vet_name, vetStatus=1)
            if existing_vet.exists():
                return_value["code"] = 406  # 406: vet already exists
                return_value["msg"] = "Vet already exists"
                return_value["data"] = {}

            else:
                # Create vet
                new_vet = models_map.MapVetInfo.objects.create(vetName=vet_name, latitude=latitude, longitude=longitude, address=address, vetDescription=vetDescription)

                # Return created vet information
                return_value["code"] = 200
                return_value["msg"] = "Vet created successfully"
                return_value["data"] = new_vet.toDict()

        except Exception as e:
            return_value["code"] = 413
            return_value["msg"] = "Error"
            print(e)

        return JsonResponse(return_value)


class VetListView(APIView):
    def post(self, request, *args, **kwargs):
        return_value = {"code": None, "msg": None, "data": None}
        user_id = json.loads(request.body).get("userId")

        try:
            # check user exist
            user_check = models_user.UserInfo.objects.filter(userId=user_id, userStatus=1)
            if user_check.exists():
                vet_search = models_map.MapVetInfo.objects.filter(vetStatus=1)
                if vet_search.exists():
                    data = []
                    for vet in vet_search:
                        vet_dict = vet.toDict()
                        userId = user_check[0].userId
                        if User.objects.get(id=userId).is_staff:  # admin user
                            vet_dict["isEditable"] = 1
                        else:
                            vet_dict["isEditable"] = 2
                        data.append(vet_dict)

                    # Return vet info
                    return_value["code"] = 200
                    return_value["msg"] = "Vet info found"
                    return_value["data"] = data
                else:  # no vet found
                    return_value["code"] = 201
                    return_value["msg"] = "No vet found"
                    return_value["data"] = {}
            else:
                return_value["code"] = 401
                return_value["msg"] = "User not found"
                return_value["data"] = {}
        except Exception as e:
            print(e)
        return JsonResponse(return_value)


class VetSearchView(APIView):
    def post(self, request, *args, **kwargs):
        return_value = {"code": None, "msg": None, "data": None}

        # Get search keyword from request
        search_keyword = json.loads(request.body).get("searchKeyword")

        try:
            # Search vet
            vet_search = models_map.MapVetInfo.objects.filter(Q(vetName__contains=search_keyword) | Q(address__contains=search_keyword) | Q(vetDescription__contains=search_keyword))
            vet_list = []

            # Check if search result exists
            if vet_search.exists():
                # convert vet object to dict
                for vet in vet_search:
                    vet_dict = vet.toDict()
                    vet_list.append(vet_dict)

                # return success message
                return_value["code"] = 200
                return_value["msg"] = "Search successful"

            else:
                return_value["code"] = 201
                return_value["msg"] = "No vets found"

            # return search result
            return_value["data"] = vet_list

        except Exception as e:
            return_value["code"] = 413
            return_value["msg"] = "Error"
            print(e)

        return JsonResponse(return_value)

# Views template
class UserProfileListView(ModelViewSet): 
    # authentication_classes = [
    #     Authentication,
    # ]
    queryset = models_user.UserInfo.objects.all()
    serializer_class = user_infomation_ser.UserInfoSer
