# Generated by Django 5.1.3 on 2025-02-05 06:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('client', '0010_otp_purpose'),
    ]

    operations = [
        migrations.AddField(
            model_name='otp',
            name='is_used',
            field=models.BooleanField(default=False),
        ),
    ]
