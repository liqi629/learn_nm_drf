
import os
import json
from datetime import datetime

from django.conf import settings
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.viewsets import ModelViewSet
from rest_framework import permissions

from apps.interfaces.models import Interfaces
from apps.testcases.models import Testcases
from apps.envs.models import Envs
from apps.testcases.serializers import TestcasesSerializer, TestcasesRunSerializer


from utils import handle_datas
from utils import common


class TestcasesViewSet(ModelViewSet):
    """
    create:
    创建用例

    retrieve:
    获取用例详情数据

    update:
    更新用例

    partial_update:
    部分更新用例

    destroy:
    删除用例

    list:
    获取用例列表数据

    run:
    通过套件运行数据
    """
    queryset = Testcases.objects.filter(is_delete=False)
    serializer_class = TestcasesSerializer
    ordering_fields = ['name']
    filterset_fields = ['id','name']



    def perform_destory(self,instance):
        instance.is_delete = True
        instance.save()

    def retrieve(self, request, *args, **kwargs):
        """获取用例详情"""
        #Testcase对象
        testcase_obj = self.get_object()

        # 用例前置信息
        testcase_include = json.loads(testcase_obj.include,encoding='utf-8')

        # 用例请求信息
        testcase_request = json.loads(testcase_obj.request,encoding='utf-8')
        testcase_request_datas = testcase_request.get('test').get('request')

        # 处理用例的validate列表 断言
        testcase_validate = testcase_request.get('test').get('validate')
        testcase_validate_list = handle_datas.handle_data1(testcase_validate)

        # 处理用例param数据
        testcase_param = testcase_request_datas.get('param')
        testcase_param_list = handle_datas.handle_data4(testcase_param)

        # 处理用例header数据
        testcase_header = testcase_request_datas.get('header')
        testcase_header_list = handle_datas.handle_data4(testcase_header)

        #处理用例的variables列表
        testcase_variables = testcase_request.get('test').get('variables')
        testcase_variables_list = handle_datas.handle_data2(testcase_variables)

        #处理form表单数据
        testcase_form_datas = testcase_request_datas.get('data')
        testcase_form_datas_list = handle_datas.handle_data4(testcase_form_datas)

        # 处理json数据
        testcase_json_datas = json.dumps(testcase_request_datas.get('json'),ensure_ascii=False)

        # 处理extract数据
        testcase_extract_datas = testcase_request.get('test').get('extract')
        testcase_extract_datas_list = handle_datas.handle_data3(testcase_extract_datas)

        #处理parameters数据
        testcase_parameters_datas = testcase_request.get('test').get('parameters')
        testcase_parameters_datas_list = handle_datas.handle_data3(testcase_parameters_datas)

        # 处理setupHooks数据
        testcase_setup_hooks_datas = testcase_request.get('test').get('setup_hooks')
        testcase_setup_hooks_datas_list = handle_datas.handle_data5(testcase_setup_hooks_datas)

        # 处理teardownHooks数据

        testcase_teardown_hooks_datas = testcase_request.get('test').get('teardown_hooks')
        testcase_teardown_hooks_datas_list = handle_datas.handle_data5(testcase_teardown_hooks_datas)

        selected_configure_id = testcase_include.get('config')
        selected_interface_id = testcase_obj.interface_id
        selected_project_id = Interfaces.objects.get(id=selected_interface_id).project_id
        selected_testcase_id = testcase_include.get('testcases')

        datas = {
            "author":testcase_obj.author,
            "testcase_name":testcase_obj.name,
            "selected_configure_id":selected_configure_id,
            "selected_interface_id":selected_interface_id,
            "selected_project_id":selected_project_id,
            "selected_testcase_id":selected_testcase_id,

            "method":testcase_request_datas.get('method'),
            "url":testcase_request_datas.get('url'),
            "param":testcase_param_list,
            "header":testcase_header_list,
            "variable":testcase_form_datas_list,
            "jsonVariable":testcase_json_datas,

            "extract":testcase_extract_datas_list,
            "validate":testcase_validate_list,
            "globalVar":testcase_variables_list,
            "parameterized":testcase_parameters_datas_list,
            "setupHooks":testcase_setup_hooks_datas_list,
            "teardownHooks":testcase_teardown_hooks_datas_list,

        }

        return Response(datas)

    @action(methods=['post'],detail=True)
    def run(self,request,*args,**kwargs):

        instance = self.get_object()
        serializer = self.get_serializer(instance,data = request.data)
        serializer.is_valid(raise_exception=True)
        datas = serializer.validated_data

        env_id = datas.get('env_id')
        # 指定测试文件存放目录 suites+时间
        testcase_dir_path = os.path.join(settings.SUITES_DIR,datetime.strftime(datetime.now(),'%Y%m%d%H%M%S%f'))
        # 创建文件夹
        os.mkdir(testcase_dir_path)
        # 获取环境
        env = Envs.objects.filter(id=env_id,is_delete=False).first()

        # 生成yaml用例文件
        common.generate_testcase_files(instance,env,testcase_dir_path)
        #运行用例
        return common.run_testcase(instance,testcase_dir_path)
    def get_serializer_class(self):
        # 三元运算，如果run 返回前面的，否则返回后面的
        return TestcasesRunSerializer if self.action == 'run' else self.serializer_class

