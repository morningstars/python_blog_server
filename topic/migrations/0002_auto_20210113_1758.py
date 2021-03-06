# Generated by Django 3.1.5 on 2021-01-13 09:58

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0001_initial'),
        ('topic', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='topic',
            name='author',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='user.userprofile', verbose_name='作者'),
        ),
        migrations.AlterField(
            model_name='topic',
            name='category',
            field=models.CharField(max_length=20, verbose_name='分类'),
        ),
        migrations.AlterField(
            model_name='topic',
            name='limit',
            field=models.CharField(max_length=10, verbose_name='权限'),
        ),
    ]
