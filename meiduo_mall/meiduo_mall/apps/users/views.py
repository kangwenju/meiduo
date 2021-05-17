from django.shortcuts import render
from rest_framework import status
from rest_framework.generics import GenericAPIView, CreateAPIView
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.mixins import CreateModelMixin

from users.models import User
from users.serializers import UserSerializer
# Create your views here.

# POST /users/


class UserView(CreateAPIView):
    # 指定视图所使用的序列化器类
    serializer_class = UserSerializer

    # def post(self, request):
    #     """
    #     注册用户信息的保存；
    #     1.获取参数并进行校验(参数完整性, 是否同意协议， 手机号格式, 手机号是否存在, 两次密码是否一致, 短信验证码是否正确)
    #     2.创建新用户并保存到数据库
    #     3.注册成功, 将新用户序列化并返回
    #     """
    #     # 1.获取参数并进行校验(参数完整性, 是否同意协议， 手机号格式, 手机号是否存在, 两次密码是否一致, 短信验证码是否正确)
    #     serializer = self.get_serializer(data=request.data)
    #     serializer.is_valid(raise_exception=True)
    #
    #     # 2.创建新用户并保存到数据库(create)
    #     serializer.save()
    #
    #     # 3.注册成功, 将新用户序列化并返回
    #     return Response(serializer.data, status=status.HTTP_201_CREATED)


# GET /users/usernames/(?P<username>\w{5,20})/count/


class UsernameCountView(APIView):
    def get(self, request, username):
        """
        获取用户名数量:
        1.根据用户名查询数据库, 获取查询结果数量
        2.返回用户名数量
        """
        # 1.根据用户名查询数据库, 获取查询结果数量
        count = User.objects.filter(username=username).count()

        # 2.返回用户名数量
        res_data = {
            'username': username,
            'count': count
        }
        return Response(res_data)

# GET /mobiles/(?P<mobile>1[3-9]\d{9})/count/


class MobileCountView(APIView):
    def get(self, request, mobile):
        """
        获取手机号数量:
        1.根据手机号查询数据库, 获取查询结果数量
        2.返回手机号数量
        """
        # 1.根据手机号查询数据库, 获取查询结果数量
        count = User.objects.filter(mobile=mobile).count()

        # 2.返回手机号数量
        res_data = {
            'mobile': mobile,
            'count': count
        }
        return Response(res_data)