
from django.urls import path, include
# from projects.views import index
from apps.projects import views

from rest_framework.documentation import include_docs_urls

from rest_framework import routers

#1.创建路由对象
router = routers.SimpleRouter()
# 使用下面得路由，会在根 路径列出url信息
# router = routers.DefaultRouter()

# 2.注册路由.第一个参数prefix为路由前缀，一般添加应用名即可。
# 第二个参数viewset 视图集类，不要加as_view()
router.register(r'projects', views.ProjectsViewSet)

# router = DefaultRouter()
# router.register(r'projects', views.ProjectsViewSet)

urlpatterns = [
    # path('', index),
    # 类试图，path第二个参数为类视图名.as_view()
    # path('', views.IndexView.as_view()),
    # 尖括号<>代表一个命名参数。 int为路径参数类型转换器，pk参数别名。自带的类型int slug uuid
    # path('<int:pk/>',views.IndexView.as_view())

    # path('projects/', views.ProjectsList.as_view()),
    # path('projects/<int:pk>/', views.ProjectsDetail.as_view()),
    # path('projects/',views.ProjectsViewSet.as_view({
    #     'get':'list',
    #     'post':'create',
    # }),name ='project-list'),
    # path('projects/<int:pk>/',views.ProjectsViewSet.as_view({
    #     'get':'retrieve',
    #     'put': 'update',
    #     'delete': 'destroy',
    # })),
    # path('projects/names/', views.ProjectsViewSet.as_view({
    #     'get': 'names',
    # }),name ='project-names'),
    # path('projects/<int:pk>/interfaces/',views.ProjectsViewSet.as_view({
    #     'get':'interfaces',
    # })),
    # 3.将自动生成的路由添加到这里
    path('',include(router.urls)),
    path('docs/',include_docs_urls(title='测试平台接口文档',description='接口文档')),
    path('api/',include('rest_framework.urls')),

]

# 可以放列表里面也可放在外面 这样写
# urlpatterns +=router.urls




from drf_yasg.views import get_schema_view
from drf_yasg import openapi
schema_view = get_schema_view(
    openapi.Info(
        title="接口文档平台",  # 必传
        default_version='v1',  # 必传
        description="文档描述",
        terms_of_service='',
        contact=openapi.Contact(email="1093254791@qq.com"),
        license=openapi.License(name="BSD LICENSE")
    ),
    public=True,
    # permission_classes=(permissions.)  # 权限类
)

urlpatterns += [
    # re_path(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0)),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),

]