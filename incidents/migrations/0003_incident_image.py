# Generated by Django 5.1.2 on 2024-11-05 12:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('incidents', '0002_alter_comment_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='incident',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='incident_images/'),
        ),
    ]
