import os
from datetime import datetime

from django.shortcuts import render

# Create your views here.
from rest_framework import status

from rest_framework.decorators import action

from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response

from Learn_Django import settings
from apps.configures.models import Configures
from apps.interfaces.models import Interfaces
from apps.interfaces.serializers import InterfacesModelSerializer
from apps.projects.serializers import InterfaceNameSerializer
from apps.interfaces.utils import get_count_by_project
from apps.testcases.models import Testcases
from apps.envs.models import Envs
from utils import common
from apps.interfaces import serializers


class InterfacesViewSet(ModelViewSet):
    """
    create:
    创建接口

    retrieve:
    获取接口详情数据

    update:
    更新接口

    partial_update:
    部分更新接口

    destroy:
    删除接口

    list:
    获取接口列表数据

    names:
    获取所有接口名称
    """
    queryset = Interfaces.objects.all()
    serializer_class = InterfacesModelSerializer
    ordering_fields = ['name']
    filterset_fields = ['id','name']

    # methods默认get  detail 指定该动作处理的是否为详情资源对象（url是否需要传递pk键值）
    @action(methods=['get'],detail=False)
    def names(self,request,*args,**kwargs):
        queryset = self.get_queryset()
        serializer = InterfaceNameSerializer(instance=queryset,many=True)
        return Response(serializer.data)

    @action(methods=['get'],detail=True,url_path='configs')
    def configures(self,request,pk=None):
        configures_models = Configures.objects.filter(interface_id=pk,is_delete=False)
        one_list = []
        for obj in configures_models:
            one_list.append({
                'id':obj.id,
                'name':obj.name
            })
        return Response(data=one_list)

    @action(methods=['get'], detail=True, url_path='testcases')
    def testcases(self,request,pk=None):
        testceses_models = Testcases.objects.filter(interface_id=pk,is_delete=False)
        one_list = []
        for obj in testceses_models:
            one_list.append({
                'id':obj.id,
                'name':obj.name,
                'status_code':200
            })
        return Response(data=one_list)

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page,many=True)
            datas = serializer.data
            datas = get_count_by_project(datas)
            return self.get_paginated_response(datas)

        serializer = self.get_serializer(queryset,many=True)
        datas = serializer.data
        datas = get_count_by_project(datas)
        return Response(datas)

    def perform_destory(self,instance):
        instance.is_delete = True
        instance.save()

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
        testcase_objs = Testcases.objects.filter(is_delete=False,interface=instance)
        if not testcase_objs.exists(): #如果接口下没有接口则无法运行
            data_dict = {
                "detail":"此接口下无接口，无法运行！"
            }
            return Response(data_dict,status=status.HTTP_400_BAD_REQUEST)

        for one_obj in testcase_objs:

            # 生成yaml用例文件
            common.generate_testcase_files(one_obj, env, testcase_dir_path)
        # 运行用例
        return common.run_testcase(instance, testcase_dir_path)

    def get_serializer_class(self):
        if self.action=='run':

            return serializers.InterfacesRunSerializer
        else:
            return self.serializer_class