# Generated by Django 3.2.11 on 2022-01-09 02:41

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0002_auto_20220109_1005'),
    ]

    operations = [
        migrations.RenameField(
            model_name='comment',
            old_name='mjoin',
            new_name='mJoin',
        ),
    ]
