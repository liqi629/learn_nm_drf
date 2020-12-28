
from django.urls import path
from projects.views import index
from projects import views

from rest_framework.routers import DefaultRouter



# router = DefaultRouter()
# router.register(r'projects', views.ProjectsViewSet)

urlpatterns = [
    # path('', index),
    # 类试图，path第二个参数为类视图名.as_view()
    path('', views.IndexView.as_view()),
    # 尖括号<>代表一个命名参数。 int为路径参数类型转换器，pk参数别名。自带的类型int slug uuid
    # path('<int:pk/>',views.IndexView.as_view())

    # path('projects/', views.ProjectsList.as_view()),
    # path('projects/<int:pk>/', views.ProjectsDetail.as_view()),
    path('projects/',views.ProjectsViewSet.as_view({
        'get':'list',
        'post':'create',
    }),name ='project-list'),
    path('projects/<int:pk>/',views.ProjectsViewSet.as_view({
        'get':'retrieve',
        'put': 'update',
        'delete': 'destroy',
    })),
    path('projects/names', views.ProjectsViewSet.as_view({
        'get': 'names',
    }),name ='project-list'),

]


# urlpatterns +=router.urls