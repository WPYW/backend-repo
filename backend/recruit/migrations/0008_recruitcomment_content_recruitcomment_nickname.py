# Generated by Django 4.1.3 on 2023-03-07 15:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("recruit", "0007_rename_view_recruit_views"),
    ]

    operations = [
        migrations.AddField(
            model_name="recruitcomment",
            name="content",
            field=models.CharField(default="", max_length=200),
        ),
        migrations.AddField(
            model_name="recruitcomment",
            name="nickname",
            field=models.CharField(default="", max_length=200),
        ),
    ]
