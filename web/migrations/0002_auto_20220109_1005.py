# Generated by Django 3.2.11 on 2022-01-09 02:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='class',
            name='cCode',
        ),
        migrations.AlterField(
            model_name='class',
            name='id',
            field=models.CharField(max_length=4, primary_key=True, serialize=False, verbose_name='課程代碼'),
        ),
    ]