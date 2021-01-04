

from rest_framework import serializers

from apps.projects.models import Projects
from apps.interfaces.models import Interfaces
from apps.debugtalks.models import DeubgTalks



class ProjectModelSerializer(serializers.ModelSerializer):


    class Meta:
        model = Projects

        exclude = ('update_time','is_delete')
        extar_kwargs = {
            'create_time':{
                'read_only':True,
            }
        }

    def create(self, validated_data):
        project_obj = super().create(validated_data)
        DeubgTalks.objects.create(project=project_obj)
        return project_obj

class ProjectNameSerializer(serializers.ModelSerializer):
    class Meta:
        model = Projects
        fields = ('id','name')

class InterfaceNameSerializer(serializers.ModelSerializer):
    class Meta:
        model = Interfaces
        fields = ('id', 'name','tester')

class InterfacesByProjectIdSerializer(serializers.ModelSerializer):

    interfaces = InterfaceNameSerializer(read_only=True,many=True)
    class Meta:
        model = Projects
        fields = ('id','interfaces')


