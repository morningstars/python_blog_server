from django.db import models
from user.models import UserProfile

# Create your models here.


'''
迁移指定模块
python3 manage.py makemigrations topic
python3 manage.py migrate topic
'''


class Topic(models.Model):
    # 主键为id django默认自动添加
    title = models.CharField('题目', max_length=50)
    category = models.CharField('分类', max_length=20)
    limit = models.CharField('权限', max_length=10)
    # auto_now_add 创建时间的时间戳
    # auto_now 每次保存对象时 自动更新时间戳
    create_time = models.DateTimeField('创建时间', auto_now_add=True)
    modify_time = models.DateTimeField('修改事件', auto_now=True)
    content = models.TextField('博客内容')
    introduce = models.CharField('博客内容介绍', max_length=90)

    author = models.ForeignKey(UserProfile, null=True, on_delete=models.CASCADE, verbose_name='作者')

    class Meta:
        db_table = 'topic'
