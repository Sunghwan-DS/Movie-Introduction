# Generated by Django 2.1.15 on 2020-06-17 08:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0011_auto_20200615_1722'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='rrn',
            field=models.IntegerField(default=0),
        ),
    ]
