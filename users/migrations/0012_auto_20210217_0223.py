# Generated by Django 3.1.6 on 2021-02-17 10:23

from django.db import migrations
import imagekit.models.fields


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0011_auto_20210216_0123'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='image',
            field=imagekit.models.fields.ProcessedImageField(default='default.jpg', upload_to='profilePics'),
        ),
    ]
