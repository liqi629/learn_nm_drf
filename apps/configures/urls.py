


from rest_framework import routers
from apps.configures.views import ConfiguresViewSet


router = routers.DefaultRouter()

router.register(r'configures', ConfiguresViewSet)


urlpatterns = [

]
urlpatterns +=router.urls
