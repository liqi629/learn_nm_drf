


from rest_framework import routers
from apps.testsuites.views import TestsuitsViewSet


router = routers.DefaultRouter()

router.register(r'testsuites', TestsuitsViewSet)


urlpatterns = [

]
urlpatterns +=router.urls
