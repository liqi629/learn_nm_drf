
import re

from rest_framework import serializers

from django.contrib.auth.models import User
from rest_framework_jwt.settings import api_settings
from rest_framework.validators import UniqueValidator

class RegisterSerializer(serializers.ModelSerializer):

    password_confirm = serializers.CharField(label='确认密码',
                                             max_length=20,
                                             min_length=6,
                                             help_text='确认密码',
                                             error_messages={
                                                 'min_length':'仅允许6~20个字符',
                                                 'max_length':'仅允许6~20个字符'},
                                             write_only=True)
    token = serializers.CharField(label='生成token',help_text='生成token',read_only=True)

    class Meta:
        model = User
        # fields ="__all__"

        fields = ('id', 'username', 'password', 'email',
                  'password_confirm', 'token')
        # model中没有的字段，不能在extra_kwargs 指定
        #使用extra_kwargs参数为ModelSerializer添加或修改原有的选项参数---字典格式。
        #如果字段已在序列化程序类中显式声明，则该extra_kwargs选项将被忽略。
        extra_kwargs = {
            'username':{
                'label':'用户名',
                'help_text':'用户名',
                'min_length': 6,
                'max_length': 20,
                'error_messages': {'min_length': '仅允许6~20个字符',
                                  'max_length': '仅允许6~20个字符',}
            },
            'email':{
                'label': '邮箱',
                'help_text': '邮箱',
                'write_only':True,
                'required':True,  #必传
                # 邮箱重复校验
                'validators': [UniqueValidator(queryset=User.objects.all(), message='此邮箱已注册')]
            },
            'password': {
                'label': '密码',
                'help_text': '密码',
                'min_length': 6,
                'max_length': 20,
                'write_only': True,
                'error_messages': {'min_length': '仅允许6~20个字符',
                                   'max_length': '仅允许6~20个字符', }
            }
        }
    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')
        password_confirm = attrs.get('password_confirm')
        if not re.match(r'^([A-Za-z0-9]+@[a-zA-Z0-9]+\.[a-zA-Z0-9_-]+)$', email):
            raise serializers.ValidationError('邮箱格式不正确！')
        if password != password_confirm:
            raise serializers.ValidationError('两次输入的密码不一致！')
        return attrs


    def create(self,validated_data):
        validated_data.pop('password_confirm')
        # print(validated_data)
        # create_user会对密码进行加密
        user = User.objects.create_user(**validated_data)
        # 手动创建token
        jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
        jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER

        payload = jwt_payload_handler(user)
        token = jwt_encode_handler(payload)
        user.token = token
        return user