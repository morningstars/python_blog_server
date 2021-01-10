from django.db import models


# Create your models here.

class UserProfile(models.Model):
    username = models.CharField('用户名', max_length=11, primary_key=True)
    nickname = models.CharField('昵称', max_length=30)
    email = models.EmailField('邮箱', max_length=50)
    password = models.CharField('密码', max_length=40)
    sign = models.CharField('个人签名', max_length=50)
    info = models.CharField('个人描述', max_length=150)
    avatar = models.ImageField('头像', max_length=100, upload_to='avatar/')

    class Meta:
        # 指定创建的表的名称
        db_table = 'user_profile'
