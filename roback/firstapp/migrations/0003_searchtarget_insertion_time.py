# Generated by Django 4.2.6 on 2023-12-11 18:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('firstapp', '0002_searchtarget_insertion_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='searchtarget',
            name='insertion_time',
            field=models.TimeField(auto_now=True),
        ),
    ]
