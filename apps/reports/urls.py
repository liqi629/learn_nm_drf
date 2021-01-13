


from rest_framework import routers
from apps.reports.views import ReportsViewSet


router = routers.DefaultRouter()

router.register(r'reports', ReportsViewSet)


urlpatterns = [

]
urlpatterns +=router.urls
