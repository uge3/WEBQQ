from django.contrib import admin
from web import models
# Register your models here.

class CategoryAdmin(admin.ModelAdmin):#注册admin显示的字段
    list_display = ('id','name')

class ArticleAdmin(admin.ModelAdmin):#注册admin显示的字段
    list_display = ('id','title','author')


class CommentAdmin(admin.ModelAdmin):#评论
    list_display = ('id','parent_comment','comment','date')

admin.site.register(models.Article,ArticleAdmin)
admin.site.register(models.Category,CategoryAdmin)
admin.site.register(models.Comment,CommentAdmin)
admin.site.register(models.ThumbUp)
admin.site.register(models.UserProfile)
admin.site.register(models.UserGroup)