from django.db import models
from datetime import datetime
import json

"""
Models connected with databases
"""


# Pet information
class PetInfo(models.Model):
    petId = models.AutoField(primary_key=True, verbose_name="petId")
    userId = models.IntegerField(verbose_name="userId", default=None)
    petName = models.CharField(max_length=50, verbose_name="petName", default=None)
    petGender = models.CharField(max_length=50, verbose_name="petGender", default=None, null=True, blank=True)
    petAge = models.IntegerField(verbose_name="petAge", default=None, null=True, blank=True)
    petType = models.CharField(max_length=50, verbose_name="petType", default=None, null=True, blank=True)
    petBreed = models.CharField(max_length=50, verbose_name="petBreed", default=None, null=True, blank=True)
    petColor = models.CharField(max_length=50, verbose_name="petColor", default=None, null=True, blank=True)
    petTags = models.JSONField(blank=True, null=True)
    petChipInfo = models.CharField(max_length=200, verbose_name="petChipInfo", default=None, null=True, blank=True)
    vetId = models.CharField(max_length=50, verbose_name="vetId", default=None, null=True, blank=True)
    petInsurance = models.CharField(max_length=200, verbose_name="petInsurance", default=None, null=True, blank=True)
    petVaccination = models.CharField(max_length=200, verbose_name="petVaccination", default=None, null=True, blank=True)
    avatar = models.CharField(max_length=300, verbose_name="avatar", default=None, null=True, blank=True) # pet avatar
    petBirthday = models.DateField(verbose_name="petBirthday", null=True, blank=True)
    createTime = models.DateTimeField(default=datetime.now)
    modifyTime = models.DateTimeField(default=datetime.now)
    modifyPersonId = models.CharField(max_length=50, verbose_name="modifyPersonId", default=None, null=True, blank=True)
    petStatus = models.IntegerField(default=1, verbose_name="petStatus")

    def toDict(self):
        tags = json.loads(self.petTags) if self.petTags else None
        return {
            "petId": self.petId,
            "userId": self.userId,
            "petName": self.petName,
            "petGender": self.petGender,
            "petAge": self.petAge,
            "petType": self.petType,
            "petBreed": self.petBreed,
            "petColor": self.petColor,
            "petTags": tags,
            "petChipInfo": self.petChipInfo,
            "vetId": self.vetId,
            "petInsurance": self.petInsurance,
            "petVaccination": self.petVaccination,
            "avatar": self.avatar,
            "petBirthday": self.petBirthday.strftime("%Y-%m-%d") if self.petBirthday else None,
            "createTime": self.createTime.strftime("%Y-%m-%d %H:%M:%S"),
            "modifyTime": self.modifyTime.strftime("%Y-%m-%d %H:%M:%S"),
            "modifyPersonId": self.modifyPersonId,
            "petStatus": self.petStatus,
        }

    class Meta:
        db_table = "pet_info"
