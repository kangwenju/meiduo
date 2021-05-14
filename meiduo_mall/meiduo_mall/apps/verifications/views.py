import random

from django_redis import get_redis_connection
from django.shortcuts import render
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from verifications import constants
from meiduo_mall.libs.yuntongxun.sms import CCP

# 获取日志器
import logging
logger = logging.getLogger('django')

# Create your views here.


class SMSCodeView(APIView):
    def get(self, request, mobile):
        """
        获取短信验证码：
        1.随机生成6位数字作为短信验证码
        2.在redis中存储短信验证码内容，以'sms_<mobile>'位key,以验证码内容为value
        3.使用云通讯给'mobile'发送短信
        4.返回应答，短信发送成功
        :param request:
        :param mobile:
        :return:
        """
        # 判断给'mobile'60s之内是否发送过短信
        redis_conn = get_redis_connection('verify_codes')

        send_flag = redis_conn.get('send_flag_%s' % mobile)

        if send_flag:
            # 60s之内发送过短信
            return Response({'message': '发送短信过于频繁'}, status=status.HTTP_403_FORBIDDEN)

        # 1.随机生成6位数字作为短信验证码
        sms_code = '%06d' % random.randint(0, 999999)

        # 2.在redis中存储短信验证码内容，以'sms_<mobile>'位key, 以验证码内容为value
        # redis_conn.set('<key>', '<value>', '<expires>')
        # redis_conn.setex('<key>', '<expires>', '<value>')

        # 创建redis管道对象
        pl = redis_conn.pipeline()

        # 向redis管道中添加命令
        pl.setex('sms_%s' % mobile, constants.SMS_CODE_REDIS_EXPIRES, sms_code)
        pl.setex('send_flag_%s' % mobile, constants.SEND_SMS_CODE_INTERVAL, 1)

        # 一次性执行管道中的所有命令
        pl.execute()

        # 3.使用云通讯给'mobile'发送短信
        expires = constants.SMS_CODE_REDIS_EXPIRES // 60

        # 发出发送短信任务消息
        from celery_tasks.sms.tasks import send_sms_code
        send_sms_code.delay(mobile, sms_code, expires)

        # 4.返回应答，短信发送成功
        return Response({'message': 'OK'})
