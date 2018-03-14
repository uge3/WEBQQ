#!usr/bin/env python
#-*-coding:utf-8-*-
# Author calmyan 
#BBS_web_QQ 
#2017/12/30    8:47
#__author__='Administrator'
from django import forms
from django.forms import widgets as django_widgets
import os
from django.core.exceptions import ValidationError


#回复表单验证
class callForm(forms.Form):
    #文章内容
    content = forms.CharField(
        widget=django_widgets.Textarea(attrs={'class': 'kind-content'})
    )

#表单验证
class ArticleForm(forms.Form):
    title =forms.CharField(max_length=255,min_length=5)
    summary =forms.CharField(max_length=255,min_length=5)
    category_id = forms.IntegerField()
    head_img =forms.ImageField()
    content=forms.CharField(min_length=10)


#上传文件图片路径
def uploaded_img_file(request,f):
    base_img_upload_path ='static/imgs'#上传路径
    user_path ='%s/%s'%(base_img_upload_path,request.user.userprofile.id)#用户ID
    if not os.path.exists(user_path):#目录不存
        os.mkdir(user_path)#创建目录
    with open ('%s/%s'%(user_path,f.name),'wb+') as img_file:#写入文件
        for chunk in f.chunks():
            img_file.write(chunk)
    return '%s/%s'%(user_path,f.name)


#用户注册
class UserForm(forms.Form):
    #username = forms.CharField(max_length=30)
    #password = forms.CharField(max_length=50)
    #输出的用户名
    username=forms.CharField(
        min_length=6,
        max_length=20,
        error_messages={'required': '用户名不能为空.', 'min_length': "用户名长度不能小于6个字符", 'max_length': "用户名长度不能大于32个字符"},
    )
    email=forms.EmailField(
        error_messages={'required': '邮箱不能为空.','invalid':"邮箱格式错误"},#invalid 邮箱格式错误
    )
    password = forms.RegexField(
        #正则表达
        '^(?=.*[0-9])(?=.*[a-zA-Z])(?=.*[!@#$\%\^\&\*\(\)])[0-9a-zA-Z!@#$\%\^\&\*\(\)]{8,32}$',
        min_length=12,
        max_length=32,
        error_messages={'required': '密码不能为空.',
                        'invalid': '密码必须包含数字，字母、特殊字符',
                        'min_length': "密码长度不能小于8个字符",
                        'max_length': "密码长度不能大于32个字符",
                        'message':None},
    )
    confirm_password=forms.CharField(
        #正则表达
        error_messages={'required': '确认密码不能为空.',
                        'invalid': '确认密码不对',
                        },
    )
    #验证码框
    check_code = forms.CharField(
        error_messages={'required': '验证码不能为空.'},
    )

    # 验证码 校对
    # def clean_check_code(self):
    #     #获取输入的验证码                                      生成的验证码
    #     if self.request.session.get('CheckCode').upper() != self.request.POST.get('check_code').upper():
    #         #不相等  返回错误信息
    #         raise ValidationError(message='验证码错误', code='invalid')
    #     else:
    #         return self.cleaned_data['check_code']


'''

#注册验证  ajax
class RegisterForm(BaseForm, django_forms.Form):
    #输出的用户名
    username=django_fields.CharField(
        min_length=6,
        max_length=20,
        error_messages={'required': '用户名不能为空.', 'min_length': "用户名长度不能小于6个字符", 'max_length': "用户名长度不能大于32个字符"},
    )
    email=django_fields.EmailField(
        error_messages={'required': '邮箱不能为空.','invalid':"邮箱格式错误"},#invalid 邮箱格式错误
    )
    password = django_fields.RegexField(
        #正则表达
        '^(?=.*[0-9])(?=.*[a-zA-Z])(?=.*[!@#$\%\^\&\*\(\)])[0-9a-zA-Z!@#$\%\^\&\*\(\)]{8,32}$',
        min_length=12,
        max_length=32,
        error_messages={'required': '密码不能为空.',
                        'invalid': '密码必须包含数字，字母、特殊字符',
                        'min_length': "密码长度不能小于8个字符",
                        'max_length': "密码长度不能大于32个字符",
                        'message':None},
    )
    confirm_password=django_fields.CharField(
        #正则表达
        error_messages={'required': '确认密码不能为空.',
                        'invalid': '确认密码不对',
                        },
    )
    #验证码框
    check_code = django_fields.CharField(
        error_messages={'required': '验证码不能为空.'},
    )

    #内置勾子
    #用户名重复查询
    def clean_username(self):
        #查询是否存在
        username=self.cleaned_data['username']
        u =models.UserInfo.objects.filter(username=username).count()
        if not u:
            return self.cleaned_data['username']
        else:
            raise ValidationError(message='用户名已经存在',code='invalid')
    #邮箱重复查询
    def clean_email(self):
        email=self.cleaned_data['email']
        e=models.UserInfo.objects.filter(email=email).count()
        if not e:
            return  self.cleaned_data['email']
        else:
            raise ValidationError('邮箱已经被注册!',code='invalid')
    # 验证码 校对
    def clean_check_code(self):
        #获取输入的验证码                                      生成的验证码
        if self.request.session.get('CheckCode').upper() != self.request.POST.get('check_code').upper():
            #不相等  返回错误信息
            raise ValidationError(message='验证码错误', code='invalid')
        else:
            return self.cleaned_data['check_code']
    #确认密码
    def clean_confirm_password(self):
        pwd=self.request.POST.get('password')
        pwd2=self.cleaned_data['confirm_password']
        if pwd != pwd2:
            raise ValidationError('二次输入密码不匹配')
        else:
            return self.cleaned_data['confirm_password']

'''