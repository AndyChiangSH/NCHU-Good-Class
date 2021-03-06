# Generated by Django 3.2.11 on 2022-01-10 09:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0006_auto_20220110_0038'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='mCool',
            field=models.DecimalField(decimal_places=0, default=0, max_digits=2, verbose_name='涼'),
        ),
        migrations.AlterField(
            model_name='comment',
            name='mFun',
            field=models.DecimalField(decimal_places=0, default=0, max_digits=2, verbose_name='有趣'),
        ),
        migrations.AlterField(
            model_name='comment',
            name='mJoin',
            field=models.DecimalField(decimal_places=0, default=0, max_digits=2, verbose_name='參與'),
        ),
        migrations.AlterField(
            model_name='comment',
            name='mLearn',
            field=models.DecimalField(decimal_places=0, default=0, max_digits=2, verbose_name='學習'),
        ),
        migrations.AlterField(
            model_name='comment',
            name='mSweet',
            field=models.DecimalField(decimal_places=0, default=0, max_digits=2, verbose_name='甜'),
        ),
    ]
