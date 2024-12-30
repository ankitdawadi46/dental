# Generated by Django 5.1.3 on 2024-12-27 07:35

import client.models
import django.core.validators
import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('client', '0002_alter_customuser_first_name_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('last_modified_date', models.DateTimeField(auto_now=True)),
                ('deleted_at', models.DateTimeField(blank=True, null=True)),
                ('photo', models.FileField(null=True, upload_to=client.models.profile_directory_path, validators=[django.core.validators.FileExtensionValidator(allowed_extensions=['jpg', 'png', 'jpeg', 'heic', 'svg'])])),
                ('dob', models.DateField(blank=True, null=True, verbose_name='Date of Birth')),
                ('gender', models.CharField(blank=True, choices=[('Male', 'Male'), ('Female', 'Female'), ('Other', 'Other')], max_length=50, null=True, verbose_name='Gender')),
                ('profile_type', models.CharField(blank=True, choices=[('Doctor', 'Doctor'), ('Intern', 'Intern'), ('Helper', 'Helper'), ('Client', 'Client')], max_length=30, null=True, verbose_name='Profile Type')),
                ('designation', models.CharField(blank=True, max_length=50, null=True, verbose_name='Designation')),
                ('address', models.CharField(blank=True, max_length=50, null=True, verbose_name='Address')),
                ('phone_number', models.CharField(blank=True, max_length=15, null=True, verbose_name='Phone Number')),
                ('nmc_no', models.CharField(blank=True, max_length=30, null=True, verbose_name='NMC No')),
                ('nhpc_no', models.CharField(blank=True, max_length=30, null=True, verbose_name='NHPC No')),
                ('created_by', models.ForeignKey(default=None, editable=False, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='%(class)s_createdby', to=settings.AUTH_USER_MODEL)),
                ('user', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='user_profile', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'Profile',
            },
        ),
    ]
