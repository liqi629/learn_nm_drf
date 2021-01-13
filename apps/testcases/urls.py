


from rest_framework import routers
from apps.testcases.views import TestcasesViewSet


router = routers.DefaultRouter()

router.register(r'testcases', TestcasesViewSet)


urlpatterns = [

]
urlpatterns +=router.urls
