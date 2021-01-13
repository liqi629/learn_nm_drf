


from rest_framework import routers
from apps.debugtalks.views import DebugTalksViewSet


router = routers.DefaultRouter()

router.register(r'debugtalks', DebugTalksViewSet)


urlpatterns = [

]
urlpatterns +=router.urls
