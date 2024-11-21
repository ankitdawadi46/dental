# Generated by Django 5.1.2 on 2024-10-17 09:53

import django.db.models.deletion
import django_tenants.postgresql_backend.base
import timezone_field.fields
import uuid
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('django_celery_beat', '0018_improve_crontab_helptext'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Client',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('schema_name', models.CharField(db_index=True, max_length=63, unique=True, validators=[django_tenants.postgresql_backend.base._check_schema_name])),
                ('timezone', timezone_field.fields.TimeZoneField(default='UTC')),
                ('name', models.CharField(max_length=1024, verbose_name='business name')),
                ('paid_until', models.DateTimeField(blank=True, null=True)),
                ('contact_number', models.CharField(blank=True, max_length=20, null=True)),
                ('contact_person', models.CharField(blank=True, max_length=255, null=True)),
                ('email', models.EmailField(blank=True, max_length=254, null=True)),
                ('is_enabled', models.BooleanField(default=True)),
                ('on_trial', models.BooleanField(default=False)),
                ('primary_domain_name', models.CharField(blank=True, max_length=512, null=True)),
                ('created_on', models.DateField(auto_now_add=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='SoftwareFeatures',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('deleted_at', models.DateTimeField(blank=True, null=True)),
                ('name', models.CharField(max_length=255)),
                ('identifier_slug', models.SlugField()),
            ],
            options={
                'verbose_name': 'Software Feature',
                'verbose_name_plural': 'Software Features',
            },
        ),
        migrations.CreateModel(
            name='Domain',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('domain', models.CharField(db_index=True, max_length=253, unique=True)),
                ('is_primary', models.BooleanField(db_index=True, default=True)),
                ('ns_records', models.JSONField(blank=True, null=True)),
                ('zone_id', models.CharField(blank=True, max_length=512, null=True)),
                ('is_display_domain', models.BooleanField(default=False)),
                ('tenant', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='domains', to='client.client')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Invoice',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('deleted_at', models.DateTimeField(blank=True, null=True)),
                ('paid_fee', models.BigIntegerField()),
                ('next_payment_due_date', models.DateField()),
                ('transaction_id', models.UUIDField(default=uuid.uuid4)),
                ('client', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='client.client')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ('next_payment_due_date',),
            },
        ),
        migrations.CreateModel(
            name='Payment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('deleted_at', models.DateTimeField(blank=True, null=True)),
                ('agreed_fee', models.BigIntegerField()),
                ('paid_fee', models.BigIntegerField()),
                ('enroll_date', models.DateField()),
                ('payment_due_date', models.DateField()),
                ('active_status', models.BooleanField(default=False)),
                ('additional_note', models.TextField(blank=True, null=True)),
                ('additional_contact_no', models.BigIntegerField(blank=True, null=True)),
                ('campaign_id', models.IntegerField(blank=True, null=True)),
                ('client', models.OneToOneField(on_delete=django.db.models.deletion.DO_NOTHING, to='client.client')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='PeriodicTaskTenantLink',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('use_tenant_timezone', models.BooleanField(default=False)),
                ('periodic_task', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='periodic_task_tenant_link', to='django_celery_beat.periodictask')),
                ('tenant', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='periodic_task_tenant_links', to='client.client')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='client',
            name='available_features',
            field=models.ManyToManyField(blank=True, null=True, to='client.softwarefeatures'),
        ),
    ]
