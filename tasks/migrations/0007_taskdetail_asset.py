# Generated by Django 5.1.5 on 2025-02-27 06:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0006_delete_employee'),
    ]

    operations = [
        migrations.AddField(
            model_name='taskdetail',
            name='asset',
            field=models.ImageField(blank=True, null=True, upload_to='tasks_asset'),
        ),
    ]
