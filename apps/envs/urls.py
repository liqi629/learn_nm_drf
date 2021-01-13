


from rest_framework import routers
from apps.envs.views import EnvsViewSet


router = routers.DefaultRouter()

router.register(r'envs', EnvsViewSet)


urlpatterns = [

]
urlpatterns +=router.urls
