# Generated by Django 4.1.3 on 2023-04-22 21:53

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0003_project_user_id'),
    ]

    operations = [
        migrations.RenameField(
            model_name='project',
            old_name='user_id',
            new_name='user',
        ),
    ]