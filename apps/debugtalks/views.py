from django.shortcuts import render

# Create your views here.
from rest_framework.viewsets import GenericViewSet
from rest_framework import mixins
from rest_framework import permissions
from rest_framework import filters
from rest_framework.response import Response
from .models import DeubgTalks
from .serializers import DeubgTalksSerializer


class DebugTalksViewSet(mixins.ListModelMixin,
                        mixins.UpdateModelMixin,
                        mixins.RetrieveModelMixin,
                        GenericViewSet):
    """
    list:
    返回debugtalk列表数据

    update:
    更新debugtalk

    partial_update:
    更新部分debugtalk

    """

    queryset = DeubgTalks.objects.filter(is_delete=False)
    serializer_class = DeubgTalksSerializer
    permission_classes = [permissions.IsAuthenticated, ]
    ordering_fields = ('id','project_id')

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        data_dict = {
            'id':instance.id,
            'debugtalk':instance.debugtalk
        }
        return Response(data_dict)