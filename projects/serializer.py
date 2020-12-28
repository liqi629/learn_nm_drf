

from rest_framework import serializers
from rest_framework.serializers import ModelSerializer
from rest_framework.validators import UniqueValidator

from projects.models import Projects

# 创建自定义校验器
# 第一个参数为字段的值
# def is_unique_project_name(name):
#     if '项目' not in name:
#         raise serializers.ValidationError('项目名称中必须包含“项目”')
#
#
# class ProjectSerializer(serializers.Serializer):
#     """
#     创建项目序列化器类
#     序列化器中定义的类属性字段往往与模型类字段一一对应
#     字段校验器的顺序。
#     先使用字段自己的校验即类型、长度，然后使用validators列表的校验（从左到右校验），---单字段校验，类下面的validate_name函数---最后多字段校验
#     """
#     # label 相当于label,help_text
#     # 需要输入哪些字段，那么在序列化器中就定义哪些字段
#     # 定义的序列化器字段，默认既可以进行序列化输出也可以进行反序列化输入
#     # write_only=True 指定该字段只进行反序列化输入，但不进行序列号输出
#     id= serializers.IntegerField(label='ID',read_only=True)  #read_only 该字段只读出，只能进行序列号输出
#     name = serializers.CharField(label='项目名称', max_length=200,
#                                  validators=[UniqueValidator(queryset=Projects.objects.all(),message='名称不能重复'),is_unique_project_name],
#                                  error_messages={'max_length':'长度不能超过200'}) #如果对name进行唯一约束,validators
#     leader = serializers.CharField(label='负责人', max_length=50,error_messages={'max_length':'长度不能超过50'} )
#     tester = serializers.CharField(label='测试人员', max_length=50, )
#     programer = serializers.CharField(label='开发人员', max_length=50, )
#     publish_app = serializers.CharField(label='发布应用', max_length=50, )
#     # allow_null allow_blank   相当于模型类的null和blank
#     desc = serializers.CharField(label='简要描述', allow_null=True, allow_blank=True, default='')
#     # 单字段的校验，在序列化器内部添加validate_字段名，方法 写法固定
#     # def validate_name(self,value):
#     #     pass
#     #     if not value.endswith('项目'):
#     #         raise serializers.ValidationError('项目名称必须以“项目”结尾')
#     #     # 当校验成功之后，一定要返回value
#     #     return value
#     # 多字段校验。，方法名为固定写法
#     # def validate(self,attrs):
#     #     if 'ka' not in attrs['tester'] and 'kaa' not in attrs['leader']:
#     #         raise serializers.ValidationError('ka必须是测试或者项目负责人')
#
#     def create(self, validated_data):
#         project = Projects.objects.create(**validated_data)
#         return project
#
#     def update(self, instance, validated_data):
#         instance.name = validated_data['name']
#         instance.leader = validated_data['leader']
#         instance.tester = validated_data['tester']
#         instance.programer = validated_data['programer']
#         instance.publish_app = validated_data['publish_app']
#         instance.desc = validated_data['desc']
#         instance.save()
#         return instance

    # 如果手动写了字段，就不用这个
    # class Meta:
    #     model = Projects
    #     fields = "__all__"






class ProjectModelSerializer(serializers.ModelSerializer):
    # 如果写了一个 模型类的的字段，那么 以自己写的为准


    class Meta:
        # 指定参考哪一个模型类创建
        model = Projects
        # 指定模型类哪些字段，来生成序列化器
        fields = "__all__"
        # exclude = ('name') # 除去这个，剩下的都序列化
        # read_only_fields = ('id') # 指定 只读 ，只进行序列化输出
        # extar_kwargs = {
        #     'leader':{
        #         'write_only':True,
        #         'error_messages':{'max_lenngth':'最大长度不超过xx'}
        #     },
        # }