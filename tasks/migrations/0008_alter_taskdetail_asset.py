# Generated by Django 5.1.5 on 2025-02-27 06:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0007_taskdetail_asset'),
    ]

    operations = [
        migrations.AlterField(
            model_name='taskdetail',
            name='asset',
            field=models.ImageField(blank=True, default='tasks_asset/default_img.jpg', null=True, upload_to='tasks_asset'),
        ),
    ]
