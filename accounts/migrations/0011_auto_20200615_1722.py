# Generated by Django 2.1.15 on 2020-06-15 08:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0010_auto_20200615_1657'),
    ]

    operations = [
        migrations.AlterField(
            model_name='uservisitedreview',
            name='visited_time',
            field=models.IntegerField(),
        ),
    ]
