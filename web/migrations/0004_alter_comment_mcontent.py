# Generated by Django 3.2.11 on 2022-01-09 04:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0003_rename_mjoin_comment_mjoin'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='mContent',
            field=models.TextField(max_length=1000, verbose_name='評論內容'),
        ),
    ]
