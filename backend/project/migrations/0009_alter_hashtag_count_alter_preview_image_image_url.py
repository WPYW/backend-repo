# Generated by Django 4.1.3 on 2023-02-14 06:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0008_hashtag_project_hashtag'),
    ]

    operations = [
        migrations.AlterField(
            model_name='hashtag',
            name='count',
            field=models.IntegerField(default=1),
        ),
        migrations.AlterField(
            model_name='preview_image',
            name='image_url',
            field=models.ImageField(upload_to='project_image/<django.db.models.query_utils.DeferredAttribute object at 0x000002582D6FE6E0>'),
        ),
    ]
