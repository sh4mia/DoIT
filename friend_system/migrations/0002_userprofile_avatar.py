# Generated by Django 4.2.1 on 2023-07-27 08:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('friend_system', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='avatar',
            field=models.ImageField(blank=True, null=True, upload_to=''),
        ),
    ]
