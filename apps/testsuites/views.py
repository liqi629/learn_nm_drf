import os
from datetime import datetime

from Learn_Django import settings

from rest_framework.decorators import action

from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework import permissions, status

from apps.configures.models import Configures
from apps.testsuites.models import Testsuites
from apps.testcases.models import Testcases
from apps.envs.models import Envs
from apps.testsuites.serializers import TestsuitesSerializer,TestsuitesRunSerializer

from .utils import modify_output
from testsuites.utils import get_testcases_by_interface_ids
from utils import common

class TestsuitsViewSet(ModelViewSet):
    """
    create:
    创建套件

    retrieve:
    获取套件详情数据

    update:
    更新套件

    partial_update:
    部分更新套件

    destroy:
    删除套件

    list:
    获取套件列表数据

    run:
    通过套件运行数据
    """
    queryset = Testsuites.objects.filter(is_delete=False)
    serializer_class = TestsuitesSerializer
    ordering_fields = ['id','name']
    # filterset_fields = ['id','name']



    def perform_destory(self,instance):
        instance.is_delete = True
        instance.save()

    def list(self, request, *args, **kwargs):
        response = super().list(request,*args,**kwargs)
        response.data['results'] = modify_output(response.data['results'])

        return response

    def retrieve(self, request, *args, **kwargs):
        testsuit_obj = self.get_object()
        datas = {
            "name":testsuit_obj.name,
            "project_id":testsuit_obj.project_id,
            "include":testsuit_obj.include,
        }
        return Response(datas)


    @action(methods=['post'], detail=True)
    def run(self, request, pk=None):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data)
        serializer.is_valid(raise_exception=True)
        datas = serializer.validated_data

        env_id = datas.get('env_id')
        # 指定测试文件存放目录 suites+时间
        testcase_dir_path = os.path.join(settings.SUITES_DIR, datetime.strftime(datetime.now(), '%Y%m%d%H%M%S%f'))
        # 创建文件夹
        if not os.path.exists(testcase_dir_path):
            os.mkdir(testcase_dir_path)
        # 获取环境
        env = Envs.objects.filter(id=env_id, is_delete=False).first()
        include = eval(instance.include)
        if len(include) ==0:
            data_dict = {
                "detail": "此套件下无接口，无法运行！"
            }
            return Response(data_dict, status=status.HTTP_400_BAD_REQUEST)
        # 将include中得接口id转化位此接口得用例ID
        include = get_testcases_by_interface_ids(include)

        for testcase_id in include:
            testcase_obj = Testcases.objects.filter(is_delete=False, id=testcase_id).first()


            if testcase_obj:
                # 生成yaml用例文件
                common.generate_testcase_files(testcase_obj, env, testcase_dir_path)
        # 运行用例
        return common.run_testcase(instance, testcase_dir_path)

    def get_serializer_class(self):
        # 三元运算，如果run 返回前面的，否则返回后面的
        return TestsuitesRunSerializer if self.action == 'run' else self.serializer_class