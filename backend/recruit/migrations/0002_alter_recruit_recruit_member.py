# Generated by Django 4.1.3 on 2023-03-03 16:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("recruit", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="recruit",
            name="recruit_member",
            field=models.IntegerField(),
        ),
    ]