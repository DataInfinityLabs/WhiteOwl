# Generated by Django 4.1.3 on 2023-04-09 06:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("core", "0005_remove_employee_photos_photo_employee"),
    ]

    operations = [
        migrations.AlterField(
            model_name="photo",
            name="image",
            field=models.ImageField(upload_to="media/photos/"),
        ),
    ]
