from django.db import models
from django.contrib.auth.models import User #Djago自带用户
# Create your models here.

#抽屉+虎嗅

#贴子 表
class Article(models.Model):
    '''
    贴子
    '''
    title=models.CharField(u"文章标题",max_length=255,unique=True)#不可重名,唯一(unique)
    category = models.ForeignKey("Category",verbose_name=u"版块",on_delete=models.CASCADE)#外键关联到版块
    head_img = models.ImageField(upload_to="static/imgs/uploads")#图片,当前目录下的图片目录
    summary =models.CharField(max_length=255,verbose_name='简介')
    content =models.TextField(u"内容")#文章内容,多行
    author = models.ForeignKey("UserProfile",verbose_name=u"作者",on_delete=models.CASCADE)
    publish_date =models.DateTimeField(auto_now=True)#创建时间
    hidden = models.BooleanField(default=True)#是否展示
    priority=models.IntegerField(u"优先级",default=1000)#

    def __str__(self):
        return "<%s,author:%s>"%(self.title,self.author)#标题与作者
    class Meta:
        verbose_name='贴子'
        verbose_name_plural='贴子'


#评论表
class Comment(models.Model):
    '''
    评论
    '''
    article=models.ForeignKey(Article,on_delete=models.CASCADE)#对应文章
    user=models.ForeignKey("UserProfile",on_delete=models.CASCADE)#评论人
    parent_comment =models.ForeignKey(verbose_name='回复评论', to='self',related_name='back_comment',blank=True, null=True,on_delete=models.CASCADE)#多级评论
    comment =models.TextField(max_length=1000)#评论内容 字数
    date=models.DateTimeField(auto_now=True)#评论创建时间
    def __str__(self):
        return '%s'%self.user
    class Meta:
        verbose_name='评论表'
        verbose_name_plural='评论表'

#点赞
class ThumbUp(models.Model):
    '''
    点赞
    '''
    article = models.ForeignKey('Article',verbose_name='点赞',on_delete=models.CASCADE)#对应的文章
    user =models.ForeignKey('UserProfile',on_delete=models.CASCADE)#谁点的赞
    date = models.DateTimeField(auto_now=True)#时间
    # def __str__(self):
    #     return self.user
    class Meta:
        verbose_name='点赞'
        verbose_name_plural='点赞'


#版块表
class Category(models.Model):
    '''
    版块
    '''
    name = models.CharField(u'版块',max_length=64,unique=True)#版块名
    admin = models.ManyToManyField('UserProfile')#多对多 管理员
    def __str__(self):
        return self.name
    class Meta:
        verbose_name='版块'
        verbose_name_plural='版块'

#用户表
class UserProfile(models.Model):
    '''
    帐户信息表
    '''
    user=models.OneToOneField(User,on_delete=models.CASCADE)#Djago 帐户管理 一对一
    name=models.CharField(max_length=32)#用户名
    groups=models.ManyToManyField('UserGroup')#组
    friends =models.ManyToManyField(to='self',related_name='my_friends')#朋友
    def __str__(self):
        return '%s'%self.name
    class Meta:
        verbose_name='帐户信息表'
        verbose_name_plural='帐户信息表'

#分组 角色 表
class UserGroup(models.Model):
    '''
    分组
    '''
    name=models.CharField(max_length=64,unique=True)
    def __str__(self):
        return self.name

    class Meta:
        verbose_name='分组'
        verbose_name_plural='分组'
