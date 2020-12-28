from django.db import models

# Create your models here.
class Projects(models.Model):
    """
    项目
    verbose_name：用于设置更人性化的字段名，后台管理站点
    max_length：字段最大长度
    unique:用于设置字段唯一，不能重复，默认False
    help_text：用于api文档中的一个中文名称,以及在后台管理站点缺省值的显示
    blank：设置用于前端可以不传递
    null:设置数据库中此字段允许为空
    往往blank和nulll一起使用
    default:设置默认值
    TextField:长字段，可以认为不限制字符串长度
    choices:限定取值范围
    """
    name=models.CharField(verbose_name='项目名称',max_length=200,unique=True,help_text='项目名称')
    leader=models.CharField(verbose_name='负责人',max_length=50,help_text='负责人')
    tester=models.CharField(verbose_name='测试人员',max_length=50,help_text='测试人员')
    programer=models.CharField(verbose_name='开发人员',max_length=50,help_text='开发人员')
    publish_app=models.CharField(verbose_name='发布应用',max_length=50,help_text='发布应用')
    desc=models.TextField(verbose_name='简要描述',help_text='简要描述',blank=True,default='',null=True)
    #models.IntegerField(choices=[0,1])

    #定义子类Meta，用于设置当前数据模型的元数据信息，
    class Meta:
        db_table='tb_projects'#设置表明
        verbose_name='项目'#会在admin站点中，显示一个人性化的表名
        verbose_name_plural='项目'#英文中的复数s时使用，中文名字没有复数的概念与verbose_name设置一致



# 应用：接口

class Inetrfaces(models.Model):
    """
    一个项目有多个接口，需要在多的一侧创建外键
    接口表作为字表，项目表作为父表
    ForeignKey:设置关联的模型类，内容为模型路径（应用名.模型类），也可以将应用名下的模型类导入，直接使用
    on_delete：设置的是，当父表删除之后，该字段的处理方式。CASCADE：字表也会被删除；SET_NULL，当前外键值会被设置为None，null=True；
    PROJECT，会报错；SET_DEFAULT，设置默认值，同时需要指定默认值。使用时需要把括号删除
    """
    name=models.CharField(verbose_name='接口名称',max_length=200,unique=True,help_text='接口名称')
    tester=models.CharField(verbose_name='测试人员',max_length=50,help_text='测试人员')
    desc=models.TextField(verbose_name='简要描述',help_text='简要描述',blank=True,default='',null=True)

    project=models.ForeignKey('projects.Projects',on_delete=models.CASCADE,verbose_name='所属项目',help_text='所属项目')  #数据库中，该字段未project_id
    class Meta:
        db_table='tb_interfaces'
        verbose_name='接口'
        verbose_name_plural='接口'