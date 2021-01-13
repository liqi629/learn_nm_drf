


from django.urls import path
from rest_framework import routers

from .views import SummayAPIView

urlpatterns = [
    path('summary/', SummayAPIView.as_view(), name='summary')
]

