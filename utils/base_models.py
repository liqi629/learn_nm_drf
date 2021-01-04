from django.db import models

class BaseModel(models.Model):
    """
    数据库表公共字段
    auto_now_add:当前创建日期时间
    auto_now:
    is_delets：逻辑删除标记为。default=False，逻辑删除-设置不删除
    """
    create_time = models.DateTimeField(auto_now_add=True, verbose_name="创建时间", help_text="创建时间")
    update_time = models.DateTimeField(auto_now=True, verbose_name="更新时间", help_text="更新时间")
    is_delete = models.BooleanField(default=False, verbose_name="逻辑删除", help_text="逻辑删除")

    class Meta:
        # 抽象模型类 用于其他模型来继承 数据库迁移不会创建BaseModel表
        abstract = True  # 抽象基类
        verbose_name = '公共字段表'
        db_table = 'BaseModel'