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
from django.contrib import admin
from web_chat import views


urlpatterns = [
    url(r'^board/$', views.board,name='board'),#
    url(r'^contacts/$', views.contacts,name='load_contact_list'),# 好友列表
    url(r'^send_msg/$', views.send_msg,name='send_msg'),# 发送消息
    url(r'^get_msg/$', views.get_msg,name='get_msg'),# 接收消息
]
