


from rest_framework import routers
from .views import InterfaceViewSet


router = routers.DefaultRouter()

router.register(r'interface', InterfaceViewSet)


urlpatterns = [

]
urlpatterns +=router.urls
