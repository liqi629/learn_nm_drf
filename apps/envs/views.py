from django.shortcuts import render

# Create your views here.
from django.shortcuts import render

# Create your views here.


from rest_framework.decorators import action

from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response

from apps.configures.models import Configures
from apps.envs.models import Envs
from apps.envs.serializers import EnvsModelSerializer,EnvNameSerializer

from apps.interfaces.utils import get_count_by_project
from apps.testcases.models import Testcases

class EnvsViewSet(ModelViewSet):
    """
    create:
    创建环境变量

    retrieve:
    获取环境变量详情数据

    update:
    更新环境变量

    partial_update:
    部分更新环境变量

    destroy:
    删除环境变量

    list:
    获取环境变量列表数据

    names:
    获取所有环境变量名称
    """
    queryset = Envs.objects.all()
    serializer_class = EnvsModelSerializer
    ordering_fields = ['name']
    filterset_fields = ['id','name']

    # methods默认get  detail 指定该动作处理的是否为详情资源对象（url是否需要传递pk键值）
    @action(methods=['get'],detail=False)
    def names(self,request,*args,**kwargs):
        queryset = self.get_queryset()
        serializer = EnvNameSerializer(instance=queryset,many=True)
        return Response(serializer.data)



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
