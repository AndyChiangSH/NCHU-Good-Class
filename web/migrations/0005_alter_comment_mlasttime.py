# Generated by Django 3.2.11 on 2022-01-09 14:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0004_alter_comment_mcontent'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='mLasttime',
            field=models.DateTimeField(auto_now=True, verbose_name='最後修改時間'),
        ),
    ]