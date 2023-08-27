from django.db import models
from datetime import datetime
import json

"""
Models connected with databases
"""


# Images
class Images(models.Model):
    imageId = models.AutoField(primary_key=True, verbose_name="imageId")  # imageId
    createTime = models.DateTimeField(default=datetime.now)  # createTime
    modifyTime = models.DateTimeField(default=datetime.now)  # modifyTime
    modifyPersonId = models.CharField(max_length=200, verbose_name="modifyPersonId", default=None, null=True, blank=True)  # modifyPersonId
    category = models.IntegerField(default=1, verbose_name="category")  # category: 1-blog, 2-pet, 3-map, 4-others
    status = models.IntegerField(default=1, verbose_name="status")  # status: 1-in use, 0-deleted

    def toDict(self):  # return as dict
        return {
            "imageId": self.imageId,
            "createTime": self.createTime.strftime("%Y-%m-%d %H:%M:%S"),
            "modifyTime": self.createTime.strftime("%Y-%m-%d %H:%M:%S"),
            "publishTime": self.createTime.strftime("%Y-%m-%d %H:%M:%S"),
            "category": self.category,
            "status": self.status,
        }

    class Meta:
        db_table = "images"  # table name


# Blog details
class BlogDetails(models.Model):
    blogId = models.AutoField(primary_key=True, verbose_name="blogId")  # blogId
    userId = models.CharField(max_length=200, verbose_name="userId", default=None)  # userId
    tag = models.CharField(max_length=100, verbose_name="title", default=None)  # tag
    title = models.CharField(max_length=200, verbose_name="title", default=None)  # title
    content = models.CharField(max_length=20000, verbose_name="content", default=None, blank=True, null=True)  # content
    createTime = models.DateTimeField(default=datetime.now)  # createTime
    modifyTime = models.DateTimeField(default=datetime.now)  # modifyTime
    publishTime = models.DateTimeField(default=datetime.now)  # publishTime
    modifyPersonId = models.CharField(max_length=200, verbose_name="modifyPersonId", default=None, null=True, blank=True)  # modifyPersonId
    status = models.IntegerField(default=1, verbose_name="status")  # status: 1-published, 2-draft, 3-deleted

    def toDict(self):  # return as dict
        return {
            "blogId": self.blogId,
            "userId": self.userId,
            "tag": self.tag,
            "title": self.title,
            "content": self.content,
            "createTime": self.createTime.strftime("%Y-%m-%d %H:%M:%S"),
            "modifyTime": self.createTime.strftime("%Y-%m-%d %H:%M:%S"),
            "publishTime": self.createTime.strftime("%Y-%m-%d %H:%M:%S"),
            "modifyPersonId": self.modifyPersonId,
        }

    class Meta:
        db_table = "blog_details"  # table name

class BlogImages(models.Model):
    imageId = models.AutoField(primary_key=True, verbose_name="imageId")  # imageId
    blogId = models.CharField(max_length=200, verbose_name="blogId", default=None, blank=True, null=True)  # blogId
    imageUrls = models.CharField(max_length=200, verbose_name="imageUrls", default=None, blank=True, null=True)  # imageUrlIds

    def toDict(self):  # return as dict
        return {
            "imageId": self.imageId,
            "blogId": self.blogId,
            "imageUrl": self.imageUrls,
        }

    class Meta:
        db_table = "blog_images"  # table name
