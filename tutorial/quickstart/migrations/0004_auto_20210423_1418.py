# Generated by Django 3.2 on 2021-04-23 04:18

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('quickstart', '0003_auto_20210423_1119'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='tweet',
            options={'ordering': ['-created']},
        ),
        migrations.DeleteModel(
            name='Dag',
        ),
    ]
