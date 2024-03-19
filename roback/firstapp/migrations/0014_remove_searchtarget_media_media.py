# Generated by Django 4.2.6 on 2024-01-16 23:48

from django.db import migrations, models
import django.db.models.deletion
import firstapp.models


class Migration(migrations.Migration):

    dependencies = [
        ('firstapp', '0013_alter_searchtarget_media'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='searchtarget',
            name='media',
        ),
        migrations.CreateModel(
            name='Media',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.TextField()),
                ('file', models.FileField(upload_to=firstapp.models.get_media_path)),
                ('search_target', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='search_target_media', to='firstapp.searchtarget')),
            ],
        ),
    ]
