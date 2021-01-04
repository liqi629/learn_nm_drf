# # Create your views here.
# from rest_framework.decorators import action
# from rest_framework.response import Response
# # from utils.pagination import PageNumberPaginationManual
# from .models import Projects
#
# from rest_framework import permissions
#
#
# from apps.projects.serializer import ProjectModelSerializer, \
#     ProjectNameSerializer,InterfacesByProjectIdSerializer
#
# """
# 下面的操作有哪些痛点
#     代码冗余
#     数据校验非常麻烦，且可复用性差
#     编码没有统一的规范
#     写的代码非常多
#     仅支持json格式传参，不支持form表单
#     仅能返回json格式数据，其他类型不支持
#     列表页视图没有分页，过滤、排序功能
# """
#
#
#
# #
# # def index(request):
# #     """
# #     index视图
# #     :param request:
# #     :return:
# #     """
# #     if request.method =='GET':
# #
# #         return HttpResponse("<h1>hello,get</h1>")
# #     elif request.method =='POST':
# #         return HttpResponse("<h1>hello,post</h1>")
# #     else:
# #         return HttpResponse("<h1>hello,其他请求</h1>")
#
#
# # # 类视图
# # class IndexView(View):
# #     """
# #     index主页类视图
# #     """
# #     def get(self, request):
# #         res = Projects.objects.all()
# #         print(res)
# #         return HttpResponse('%s'%res)
# #
# #         # datas = [
# #         #     {
# #         #         "name":'zhangsan',
# #         #         "age":12
# #         #     },
# #         #     {
# #         #         "name": 'lisi',
# #         #         "age": 16
# #         #     },
# #         #     {
# #         #         "name": 'wangwu',
# #         #         "age": 11
# #         #     }
# #         # ]
# #         # return render(request,'demo.html', locals())
# #         # return HttpResponse(content=datas,content_type='application/json', status=201)
# #     def post(self, request):
# #         return HttpResponse("<h1>hello,post</h1>")
# #
# #     def delect(self, request):
# #         return HttpResponse("<h1>hello,delete</h1>")
# #
# #     def put(self, request):
# #         return HttpResponse("<h1>hello,put</h1>")
#
#
#
#
# #APIView
# #GenericAPIView
# #ViewSet 不再支持get post put delete等请求方法,而只支持action动作
# #但是ViewSet这个类未提供get_object() get_serializer 等方法
# #所以需要继承GenericViewSet
# from rest_framework import viewsets
#
# # class ProjectsViewSet(mixins.ListModelMixin,
# #                       mixins.UpdateModelMixin,
# #                       mixins.RetrieveModelMixin,
# #                       mixins.CreateModelMixin,
# #                       mixins.DestroyModelMixin,
# #                       viewsets.GenericViewSet):
#
# class ProjectsViewSet(viewsets.ModelViewSet):
#     """
#     list:
#     返回所有
#
#
#     create:
#     新建项目
#     """
#     queryset = Projects.objects.all()
#     serializer_class = ProjectModelSerializer
#     # filter_backends = [filters.OrderingFilter]
#     ordering_fields = ['name','leader']
#     filterset_fields = ['name','leader']
#
#     permission_classes = [permissions.IsAuthenticated]
#
#
#
#
#
#     #可以使用action装饰器来声明自定义得动作
#     #默认情况下实例方法名就是动作名
#     #methods参数用于指定该动作支持得请求方法，默认get
#     #detail用于指定该动作要处理得是否为详情资源对象（url是否需要传递pk值）
#     @action(methods=['get'],detail=False,)
#     def names(self,request,*args,**kwargs):
#         queryset = self.get_queryset()
#         serializer = ProjectNameSerializer(instance=queryset,many=True)
#         return Response(serializer.data)
#
#
#     @action(detail=True)
#     def interfaces(self,request,*args,**kwargs):
#         interface = self.get_object()   #模型类对象 并不是获取得查询集，所以不用many=true
#         serializer = InterfacesByProjectIdSerializer(instance=interface)
#         return Response(serializer.data)
#
#
#
#
#
#
#
#
# # class ProjectsList(generics.ListCreateAPIView):
# #     #1必须指定queryset
# #     queryset = Projects.objects.all()
# #     #2指定serializer_class
# #     serializer_class = ProjectModelSerializer
# #
# #
# #     # filter_backends = [filters.OrderingFilter]
# #     ordering_fields = ['name','leader']
# #
# #     filterset_fields = ['name','leader']
# #
# #
# #
# #
# # # 继承GenericAPIView基类
# # # 必须指定queryset和serializer_class
# # class ProjectsDetail(generics.RetrieveUpdateDestroyAPIView):
# #     #1必须指定queryset
# #     queryset = Projects.objects.all()
# #     #2指定serializer_class
# #     serializer_class = ProjectModelSerializer
#
#
#
#
#
#
#
#
#
#
#
#
# # class ProjectsList(GenericAPIView):
# #     #1必须指定queryset
# #     queryset = Projects.objects.all()
# #     #2指定serializer_class
# #     serializer_class = ProjectModelSerializer
# #     #3在视图类中指定过滤引擎
# #     # filter_backends = [filters.OrderingFilter]
# #     # 4指定需要排序的字段
# #     # ordering_fields = ['name','leader']
# #
# #     #第三方的开源过滤引擎
# #     #在类视图中指定过滤引擎
# #     filter_backends=[DjangoFilterBackend]
# #     # 指定需要过滤的字段
# #     filterset_fields = ['name','leader']
# #
# #     # 在某个视图中指定分页类
# #     # pagination_class = PageNumberPaginationManual
# #
# #
# #     def get(self, request):
# #         """
# #         获取项目所有
# #         """
# #         res = self.get_queryset()
# #         # 使用filter_queryset过滤查询集
# #         res = self.filter_queryset(res)
# #         # 使用paginate_queryset分页,返回查询集,分页之后的查询集
# #         page = self.paginate_queryset(res)
# #         if page is not None:
# #             serializer = self.get_serializer(instance=page, many=True)
# #             # 可以使用get_paginated_response返回
# #             return self.get_paginated_response(serializer.data)
# #         # print(res)
# #         # project_list =  []
# #         # for project in res:
# #         #     one_dict = {
# #         #         'name' : project.name,
# #         #         'leader': project.leader,
# #         #         'testter':project.tester,
# #         #         'programer':project.programer,
# #         #         'publish_app':project.publish_app,
# #         #         'desc':project.desc
# #         #     }
# #         #     project_list.append(one_dict)
# #         # many是多条数据列表数据
# #         serializer = self.get_serializer(instance=res,many=True)
# #             # 第一个参数默认只能为字典 如果设置其他类型 需要将safe设置false。
# #         # return JsonResponse(serializer.data,safe=False)
# #         # 使用APIVIEW 就用下面的Response
# #         return Response(serializer.data)
# #
# #     def post(self,request):
# #         """
# #         新增项目
# #         从前端获取json格式数据，转化为python中的类型
# #         为了严谨性，要做各种复制的校验
# #         """
# #         # 反序列化
# #         json_data = request.body.decode('utf-8')
# #         python_data = json.loads(json_data,encoding='utf-8')
# #
# #         serializer = self.get_serializer(data=python_data)
# #         # 校验前端输入的数据，serializer.is_valid
# #         # 校验成功返回True  失败返回False ,raise_exception校验失败抛出异常
# #         # 当调用完之后，才可他调用errors属性，获取校验错误提示（字典）
# #         try:
# #             serializer.is_valid(raise_exception=True)
# #         except Exception as e:
# #             return Response(serializer.is_valid.errors)
# #         # 校验成功之后的属性使用caidated_data获取.调用create返回的是模型类对象
# #         # project = Projects.objects.create(**serializer.validated_data) #使用校验成功之后的数据，如果校验失败，此处是一个空字典
# #         # 如果再创建序列化器对象的时候，只给data传参，那么调用save实际调用的是序列化器的create
# #         serializer.save()
# #         # Projects.objects.create(name=python_data['name'],
# #         #                         leader=python_data['leader'],
# #         #                         )
# #         # project = Projects.objects.create(**python_data)
# #         # # 将模型类对象转换为字段返回
# #         # one_dict = {
# #         #     'name': project.name,
# #         #     'leader': project.leader,
# #         #     'testter': project.tester,
# #         #     'programer': project.programer,
# #         #     'publish_app': project.publish_app,
# #         #     'desc': project.desc
# #         # }
# #         # 序列化输出，给到前端
# #         return Response(serializer.data)
# #
# # # 继承GenericAPIView基类
# # # 必须指定queryset和serializer_class
# # class ProjectsDetail(GenericAPIView):
# #     #1必须指定queryset
# #     queryset = Projects.objects.all()
# #     #2指定serializer_class
# #     serializer_class = ProjectModelSerializer
# #     # def get_object(self,pk):
# #     #     try:
# #     #         return  Projects.objects.get(id=pk)
# #     #     except Projects.DoesNotExist:
# #     #         raise Http404
# #
# #     def get(self, request,pk):
# #         """
# #         """
# #         #对项目id不存在 做异常捕获
# #         project = self.get_object()
# #
# #         # one_dict = {
# #         #         'name' : project.name,
# #         #         'leader': project.leader,
# #         #         'testter':project.tester,
# #         #         'programer':project.programer,
# #         #         'publish_app':project.publish_app,
# #         #         'desc':project.desc
# #         # }
# #         # 通过模型类对象或者查询集，传给instance，就可以进行序列化操作
# #         # 通过序列化器ProjectSerializer对象的data属性，就可以获取转换之后的字典
# #         # serializer = ProjectModelSerializer(instance=project)
# #             # 如果前端请求头未指定accept，那么默认返回Json格式数据
# #         #3使用get_serializer获取序列化器
# #         serializer = self.get_serializer(instance=project)
# #         return Response(serializer.data,status=201)
# #
# #     def put(self,request):
# #         # 校验pk
# #         # 获取指定id项目
# #         project = self.get_object()
# #         # 从前端获取json格式数据，反序列化
# #         json_data = request.body.decode('utf-8')
# #         python_data = json.loads(json_data,encoding='utf-8')
# #
# #         serializer = self.get_serializer(instance=project,data=python_data)
# #         try:
# #             serializer.is_valid(raise_exception=True)
# #         except Exception as e:
# #             print(serializer.errors)
# #             return Response(serializer.errors)
# #
# #         # 更新项目
# #         # project.name = serializer.validated_data['name']
# #         # project.leader = serializer.validated_data['leader']
# #         # project.tester = serializer.validated_data['tester']
# #         # project.programer = serializer.validated_data['programer']
# #         # project.publish_app = serializer.validated_data['publish_app']
# #         # project.desc = serializer.validated_data['desc']
# #         # 在创建序列化器对象时，如果同时给instance和data传参，会自动调用序列化器的update
# #         serializer.save()
# #         # 将模型类对象转换为字典
# #         # 序列化
# #         # one_dict = {
# #         #         'name' : project.name,
# #         #         'leader': project.leader,
# #         #         'testter':project.tester,
# #         #         'programer':project.programer,
# #         #         'publish_app':project.publish_app,
# #         #         'desc':project.desc
# #         # }
# #
# #         # serializer = ProjectSerializer(instance=project)
# #             # 第一个参数默认只能为字典 如果设置其他类型 需要将safe设置false
# #         return Response(serializer.data,status=201)
# #
# #     def delete(self,request,pk):
# #         # 校验pk
# #         # 获取指定id项目
# #         project = self.get_object(pk)
# #         project.delete()
# #         return Response(None,safe=False,status=204)
# #
# #
# #
