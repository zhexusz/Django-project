from django.db import models
from datetime import datetime

"""
Models connected with databases
"""


# Map Course details
class MapCourseInfo(models.Model):
    courseId = models.AutoField(primary_key=True, verbose_name="courseId")  # courseId
    courseTitle = models.CharField(max_length=200, verbose_name="courseTitle", default=None)  # courseTitle
    courseContent = models.CharField(max_length=2000, verbose_name="courseContent", default=None)  # courseContent
    courseImage = models.CharField(max_length=200, verbose_name="courseImage", default=None)  # courseImage
    createTime = models.DateTimeField(default=datetime.now)  # createTime
    courseStatus = models.IntegerField(default=1, verbose_name="courseStatus")  # courseStatus: 1-active, 2-inactive, 3-deleted

    def toDict(self):  # return as dict
        return {
            "courseId": self.courseId,
            "courseTitle": self.courseTitle,
            "courseContent": self.courseContent,
            "courseImage": self.courseImage,
            "createTime": self.createTime.strftime("%Y-%m-%d %H:%M:%S"),
            "courseStatus": self.courseStatus,
        }

    class Meta:
        db_table = "map_course_info"  # table name


# Map School information
class MapSchoolInfo(models.Model):
    schoolId = models.AutoField(primary_key=True, verbose_name="userId")  # userId
    schoolName = models.CharField(max_length=200, verbose_name="schoolName", default=None)  # schoolName
    latitude = models.CharField(max_length=200, verbose_name="latitude", default=None)  # latitude
    longitude = models.CharField(max_length=200, verbose_name="longitude", default=None)  # longitude
    createTime = models.DateTimeField(default=datetime.now)  # createTime
    schoolStatus = models.IntegerField(default=1, verbose_name="schoolStatus")  # schoolStatus: 1-active, 2-inactive, 3-deleted
    course = models.ManyToManyField(to=MapCourseInfo, through="MapSchoolCourseInfo", through_fields=("schoolId", "courseId"))
    schoolImageUrl = models.CharField(max_length=200, verbose_name="schoolImageUrl", default=None, blank=True, null=True)  # schoolImageUrl

    def toDict(self):  # return as dict
        return {
            "schoolId": self.schoolId,
            "schoolName": self.schoolName,
            "latitude": self.latitude,
            "longitude": self.longitude,
            "createTime": self.createTime.strftime("%Y-%m-%d %H:%M:%S"),
            "schoolStatus": self.schoolStatus,
            "courses": [course.toDict() for course in self.course.all()],  # 返回关联的课程信息
            "schoolImageUrl": self.schoolImageUrl,
        }

    class Meta:
        db_table = "map_school_info"  # table name


class MapSchoolCourseInfo(models.Model):
    schoolId = models.ForeignKey(MapSchoolInfo, on_delete=models.CASCADE, verbose_name="schoolId")
    courseId = models.ForeignKey(MapCourseInfo, on_delete=models.CASCADE, verbose_name="courseId")
    createTime = models.DateTimeField(default=datetime.now)  # createTime

    class Meta:
        db_table = "map_school_course_info"


# Map Vet informaton
class MapVetInfo(models.Model):
    vetId = models.AutoField(primary_key=True, verbose_name="vetId")
    vetName = models.CharField(max_length=200, verbose_name="vetName", default=None)
    latitude = models.FloatField(verbose_name="latitude", default=None)
    longitude = models.FloatField(verbose_name="longitude", default=None)
    address = models.CharField(max_length=200, verbose_name="address", default=None)
    vetDescription = models.CharField(max_length=2000, verbose_name="vetDescription", default=None)
    vetStatus = models.IntegerField(default=1, verbose_name="vetStatus")  # vetStatus: 1-active, 2-inactive, 3-deleted

    def toDict(self):
        return {
            "vetId": self.vetId,
            "vetName": self.vetName,
            "latitude": self.latitude,
            "longitude": self.longitude,
            "address": self.address,
            "vetDescription": self.vetDescription,
            "vetStatus": self.vetStatus,
        }

    class Meta:
        db_table = "map_vet_info"  # table name
