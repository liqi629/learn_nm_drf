from datetime import datetime
from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from apps.reports.models import Reports


class ReportsModelSerializer(serializers.ModelSerializer):
    """
    报告序列化器
    """



    class Meta:
        model = Reports
        exclude = ('update_time','is_delete')
        extra_kwargs = {
            'html':{
                'write_only':True
            },
            'create_time':{
                'read_only': True
            }
        }

    def create(self, validated_data):
        report_name = validated_data['name']
        validated_data['name'] = report_name+'_'+ \
                                 datetime.strftime(datetime.now(),'%Y%m%d%H%M%S')
        report = Reports.objects.create(**validated_data)
        return report
