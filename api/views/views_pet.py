# import models and serializers
from models.models import models_user
from models.models import models_pet
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


# Add pet info
class AddPetView(APIView):
    # authentication_classes = [
    #     Authentication,
    # ]

    def post(self, request, *args, **kwargs):
        return_value = {"code": None, "msg": None, "data": None}
        # Get pet info from request
        user_id = json.loads(request.body).get("userId")
        pet_name = json.loads(request.body).get("petName")
        pet_gender = json.loads(request.body).get("petGender")
        pet_age = json.loads(request.body).get("petAge")
        pet_type = json.loads(request.body).get("petType")
        pet_breed = json.loads(request.body).get("petBreed")
        pet_color = json.loads(request.body).get("petColor")
        pet_tags = json.loads(request.body).get("petTags")
        pet_chip_info = json.loads(request.body).get("petChipInfo")
        vet_id = json.loads(request.body).get("vetId")
        avatar = json.loads(request.body).get("avatar")
        pet_insurance = json.loads(request.body).get("petInsurance")
        pet_vaccination = json.loads(request.body).get("petVaccination")

        try:
            # check user exist
            check_user = models_user.UserInfo.objects.filter(userId=user_id, userStatus=1)
            if check_user.exists():
                # data serialization
                pet_tags = json.dumps(pet_tags)
                
                # Use default avatar if no avatar provided
                if avatar == "":
                    avatar = "https://bk.petopia.top/static/images/users/pet_avatar_cat.png"
                
                # Create new pet info
                pet = models_pet.PetInfo.objects.create(userId=user_id, petName=pet_name, petGender=pet_gender, petAge=pet_age, petType=pet_type, petBreed=pet_breed, petColor=pet_color, petTags=pet_tags, petChipInfo=pet_chip_info, vetId=vet_id, petInsurance=pet_insurance, petVaccination=pet_vaccination, avatar=avatar)
                data = pet.toDict()
                # Return pet info
                return_value["code"] = 200
                return_value["msg"] = "Pet info added"
                return_value["data"] = data
            else:
                return_value["code"] = 401  # 401: user not found
                return_value["msg"] = "User not found"
                return_value["data"] = {}

        except Exception as e:
            return_value["code"] = 413
            return_value["msg"] = "Error"
            print(e)

        return JsonResponse(return_value)


# Get pet info
class PetInfoView(APIView):
    def post(self, request, *args, **kwargs):
        return_value = {"code": None, "msg": None, "data": None}
        pet_id = json.loads(request.body).get("petId")

        try:
            pet_search = models_pet.PetInfo.objects.filter(petId=pet_id, petStatus=1)
            if pet_search.exists():
                data = []
                for pet in pet_search:
                    pet_dict = pet.toDict()
                    data.append(pet_dict)
                # Return pet info
                return_value["code"] = 200
                return_value["msg"] = "Pet info found"
                return_value["data"] = data
            else:  # pet not found
                return_value["code"] = 400
                return_value["msg"] = "Pet not found"
                return_value["data"] = {}
        except Exception as e:
            print(e)
        return JsonResponse(return_value)


# Pet info list
class PetInfoListView(APIView):
    def post(self, request, *args, **kwargs):
        return_value = {"code": None, "msg": None, "data": None}
        user_id = json.loads(request.body).get("userId")

        try:
            # check user exist
            user_check = models_user.UserInfo.objects.filter(userId=user_id, userStatus=1)
            if user_check.exists():
                pet_search = models_pet.PetInfo.objects.filter(userId=user_id, petStatus=1)
                if pet_search.exists():
                    print(111)
                    data = []
                    for pet in pet_search:
                        pet_dict = pet.toDict()
                        vet_id = pet.vetId.strip()
                        pet_gender = pet.petGender.strip()
                        avatar = "https://bk.petopia.top/static/images/blogs/" + pet.avatar.strip()
                        pet_dict['vetId'] = vet_id
                        pet_dict['petGender'] = pet_gender
                        pet_dict['avatar'] = avatar
                        
                        data.append(pet_dict)
                    # Return pet info
                    return_value["code"] = 200
                    return_value["msg"] = "Pets info found"
                    return_value["data"] = data
                else:  # pets not found
                    return_value["code"] = 400
                    return_value["msg"] = "Pets not found"
                    return_value["data"] = {}
            else:
                return_value["code"] = 401
                return_value["msg"] = "User not found"
                return_value["data"] = {}
        except Exception as e:
            print(e)
        return JsonResponse(return_value)


# Edit pet info
class PetInfoEditView(APIView):
    def post(self, request, *args, **kwargs):
        return_value = {"code": None, "msg": None, "data": None}

        # Get pet info from request
        pet_id = json.loads(request.body).get("petId")
        current_user_id = json.loads(request.body).get("userId")
        pet_name = json.loads(request.body).get("petName")
        pet_gender = json.loads(request.body).get("petGender")
        pet_age = json.loads(request.body).get("petAge")
        pet_type = json.loads(request.body).get("petType")
        pet_breed = json.loads(request.body).get("petBreed")
        pet_color = json.loads(request.body).get("petColor")
        pet_tags = json.loads(request.body).get("petTags")
        pet_chip_info = json.loads(request.body).get("petChipInfo")
        vet_id = json.loads(request.body).get("vetId")
        pet_insurance = json.loads(request.body).get("petInsurance")
        pet_vaccination = json.loads(request.body).get("petVaccination")

        try:
            # check user exist
            user_check = models_user.UserInfo.objects.filter(userId=current_user_id, userStatus=1)
            if user_check.exists():
                # Check whether the pet exists
                pet = models_pet.PetInfo.objects.filter(petId=pet_id, petStatus=1).first()
                # Check if the pet exists
                if pet is None:  # 400: pet not found
                    return_value["code"] = 400
                    return_value["msg"] = "Pet not found"
                    return_value["data"] = {}
                else:
                    # Get user info
                    user_id = pet.userId
                    user_info = models_user.UserInfo.objects.filter(userId=user_id, userStatus=1).first()

                    # Check if the user has permission to edit the pet
                    if int(current_user_id) == int(user_id) or User.objects.get(id=current_user_id).is_staff:
                        # Update pet information
                        if pet_name:
                            pet.petName = pet_name
                        if pet_gender:
                            pet.petGender = pet_gender
                        if pet_age:
                            pet.petAge = pet_age
                        if pet_type:
                            pet.petType = pet_type
                        if pet_breed:
                            pet.petBreed = pet_breed
                        if pet_color:
                            pet.petColor = pet_color
                        if pet_tags:
                            pet.petTags = json.dumps(pet_tags)
                        if pet_chip_info:
                            pet.petChipInfo = pet_chip_info
                        if vet_id:
                            pet.vetId = vet_id
                        if pet_insurance:
                            pet.petInsurance = pet_insurance
                        if pet_vaccination:
                            pet.petVaccination = pet_vaccination
                        pet.modifyTime = datetime.now()
                        pet.modifyPersonId = current_user_id
                        pet.save()

                        # Return updated pet information
                        return_value["code"] = 200
                        return_value["msg"] = "Pet updated successfully"
                        return_value["data"] = pet.toDict()
                    else:
                        return_value["code"] = 403  # 403: no permission to edit the pet
                        return_value["msg"] = "This user does not have permission to edit the pet info"
                        return_value["data"] = {}
            else:
                return_value["code"] = 401  # 401: user not found
                return_value["msg"] = "User not found"
                return_value["data"] = {}
        except Exception as e:
            return_value["code"] = 413
            return_value["msg"] = "Error"
            print(e)

        return JsonResponse(return_value)


# Delete pet info
class PetInfoDeleteView(APIView):
    def post(self, request, *args, **kwargs):
        return_value = {"code": None, "msg": None, "data": None}

        # Get pet id from request
        pet_id = json.loads(request.body).get("petId")
        current_user_id = json.loads(request.body).get("userId")

        try:
            # Check if the user exists
            user_check = models_user.UserInfo.objects.filter(userId=current_user_id, userStatus=1)
            if user_check.exists():
                # Check if the pet exists
                pet_check = models_pet.PetInfo.objects.filter(petId=pet_id, petStatus=1)
                if pet_check.exists():
                    user_id = list(pet_check.values_list("userId", flat=True))[0]
                    if int(user_id) == int(current_user_id) or User.objects.get(id=current_user_id).is_superuser:
                        # Delete pet record
                        pet_check.delete()
                        # Return success message
                        return_value["code"] = 200
                        return_value["msg"] = "Pet info deleted successfully"
                        return_value["data"] = {"petId": pet_id, "userId": user_id}
                    else:
                        return_value["code"] = 403
                        return_value["msg"] = "This user does not have permission to delete the pet info"
                        return_value["data"] = {}
                else:
                    return_value["code"] = 400
                    return_value["msg"] = "Pet info not found"
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


# Views templates
class UserProfileListView(ModelViewSet): 
    # authentication_classes = [
    #     Authentication,
    # ]
    queryset = models_user.UserInfo.objects.all()
    serializer_class = user_infomation_ser.UserInfoSer
