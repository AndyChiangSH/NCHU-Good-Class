# Generated by Django 3.2.11 on 2022-01-09 16:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0005_alter_comment_mlasttime'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='mCool',
            field=models.IntegerField(default=0, verbose_name='涼'),
        ),
        migrations.AlterField(
            model_name='comment',
            name='mFun',
            field=models.IntegerField(default=0, verbose_name='有趣'),
        ),
        migrations.AlterField(
            model_name='comment',
            name='mJoin',
            field=models.IntegerField(default=0, verbose_name='參與'),
        ),
        migrations.AlterField(
            model_name='comment',
            name='mLearn',
            field=models.IntegerField(default=0, verbose_name='學習'),
        ),
        migrations.AlterField(
            model_name='comment',
            name='mSweet',
            field=models.IntegerField(default=0, verbose_name='甜'),
        ),
    ]