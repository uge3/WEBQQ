from django.db import models

# Create your models here.
from web.models import UserProfile

class QQGroup(models.Model):
    name=models.CharField(max_length=64,unique=True)#群名，唯一
    description= models.CharField(max_length=255,default="空")#群简介
    members =models.ManyToManyField(UserProfile,blank=True,null=True)#成员可以为空
    admins =models.ManyToManyField(UserProfile,related_name='qqgroup_admins')#管理员
    max_member_nums=models.IntegerField(default=255)#群人数限制
    def __str__(self):
        return self.name #群名
