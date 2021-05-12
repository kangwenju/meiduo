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
        # 1.随机生成6位数字作为短信验证码
        sms_code = '%06d' % random.randint(0, 999999)
        # 2.在redis中存储短信验证码内容，以'sms_<mobile>'位key, 以验证码内容为value
        redis_conn = get_redis_connection('verify_codes')

        # redis_conn.set('<key>', '<value>', '<expires>')
        # redis_conn.setex('<key>', '<expires>', '<value>')
        redis_conn.setex('sms_%s' % mobile, constants.SMS_CODE_REDIS_EXPIRES, sms_code)

        # 3.使用云通讯给'mobile'发送短信
        expires = constants.SMS_CODE_REDIS_EXPIRES // 60
        try:
            res = CCP().send_template_sms(mobile, [sms_code, expires], constants.SEND_SMS_TEMP_ID)
        except Exception as e:
            logger.error(e)
            return Response({'message': '验证码发送异常'}, status=status.HTTP_503_SERVICE_UNAVAILABLE)
        if res != 0:
            # 短信发送失败
            return Response({'message': '验证码发送失败'}, status=status.HTTP_503_SERVICE_UNAVAILABLE)

        # 4.返回应答，短信发送成功
        return Response({'message': 'OK'})
