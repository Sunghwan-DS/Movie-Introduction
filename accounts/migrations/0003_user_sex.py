# Generated by Django 2.1.15 on 2020-06-11 08:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_auto_20200611_1732'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='sex',
            field=models.CharField(default='남', max_length=10),
        ),
    ]