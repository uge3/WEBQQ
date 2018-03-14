"""BBS_web_QQ URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.conf.urls import include
from django.contrib import admin
from web import views



urlpatterns = [
    url(r'^admin/', admin.site.urls),#管理页面
    url(r'^chat/', include('web_chat.urls')),#聊天室 APP
    url(r'^$',views.index,name='index'),#首页
    url(r'^category/(\d+)/$',views.category,name='category'),#版块
    url(r'^article/(\d+)/$',views.article_detail,name='article_detail'),#版块
    url(r'^article/new/$',views.new_article,name='new_article'),#版块
    url(r'account/logout/',views.account_logout,name='logout'),#注消
    url(r'account/login/',views.account_login,name='login'),#登陆
    url(r'account/register/',views.register,name='register'),#注册
    url(r'^check_code.html$', views.check_code),# 验证码 校对
]
