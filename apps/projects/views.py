import os
from datetime import datetime

from Learn_Django import settings
from rest_framework.viewsets import ModelViewSet
from rest_framework import permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.exceptions import NotFound
from rest_framework import status
from rest_framework.exceptions import NotFound

from apps.projects import serializers
from .models import Projects
from .utils import get_count_by_project
from apps.interfaces.models import Interfaces
from apps.testcases.models import Testcases
from apps.envs.models import Envs
from utils import common
from .serializers import ProjectsRunSerializer


class ProjectsViewSet(ModelViewSet):
    """
    list:
    返回项目-列表数据

    retrieve:
    返回项目详情数据

    update:
    更新项目

    partial_update:
    更新项目-部分

    destroy:
    删除项目

    names:
    返回所有项目ID和名称

    interfaces:
    返回某个项目的所有接口信息（ID和名称）
    """
    queryset = Projects.objects.filter(is_delete=False)
    serializer_class = serializers.ProjectModelSerializer
    # permission_classes = [permissions.IsAuthenticated]
    ordering_fields = ['name','leader']


    def perform_destroy(self, instance):
        instance.is_delete = True
        instance.save()



    @action(methods=['get'],detail=False,)
    def names(self,request,*args,**kwargs):
        queryset = self.get_queryset()
        # serializer = serializers.ProjectNameSerializer(instance=queryset,many=True)
        serializer = self.get_serializer(instance=queryset,many=True)
        return Response(serializer.data)


    @action(methods=['get'],detail=True)
    def interfaces(self,request,pk=None):
        # interface_objs = Interfaces.objects.filter(project_id=pk,is_delete=False)
        # one_list = []
        # for obj in interface_objs:
        #     one_list.append({
        #         'id':obj.id,
        #         'name':obj.name
        #     })
        # return Response(data=one_list)
        serializer =serializers.InterfacesByProjectIdSerializer(self.get_object())
        return Response(serializer.data)

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page,many=True)
            datas = serializer.data
            # datas = get_count_by_project(datas)
            return self.get_paginated_response(datas)

        serializer = self.get_serializer(queryset,many=True)
        datas = serializer.data
        # datas = get_count_by_project(datas)
        return self.get_paginated_response(datas)

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
        interface_objs = Interfaces.objects.filter(is_delete=False,project=instance)
        if not interface_objs.exists(): #如果项目下没有接口则无法运行
            data_dict = {
                "detail":"此项目下无接口，无法运行！"
            }
            return Response(data_dict,status=status.HTTP_400_BAD_REQUEST)
        for inter_obj in interface_objs:
            testcase_objs = Testcases.objects.filter(is_delete=False,interface=inter_obj)

            for one_obj in testcase_objs:

                # 生成yaml用例文件
                common.generate_testcase_files(one_obj, env, testcase_dir_path)
        # 运行用例
        return common.run_testcase(instance, testcase_dir_path)

    def get_serializer_class(self):
        if self.action=='names':
            return serializers.ProjectNameSerializer
        elif self.action =='run':
            return serializers.ProjectsRunSerializer
        else:
            return self.serializer_class