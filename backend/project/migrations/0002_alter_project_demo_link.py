# Generated by Django 4.1.3 on 2023-02-18 21:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='project',
            name='demo_link',
            field=models.CharField(max_length=200, null=True),
        ),
    ]
