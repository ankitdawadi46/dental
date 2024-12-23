# Generated by Django 5.1.3 on 2024-12-23 09:13

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('client', '0001_initial'),
        ('django_celery_beat', '0019_alter_periodictasks_options'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='invoice',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='payment',
            name='client',
            field=models.OneToOneField(on_delete=django.db.models.deletion.DO_NOTHING, to='client.client'),
        ),
        migrations.AddField(
            model_name='payment',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='periodictasktenantlink',
            name='periodic_task',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='periodic_task_tenant_link', to='django_celery_beat.periodictask'),
        ),
        migrations.AddField(
            model_name='periodictasktenantlink',
            name='tenant',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='periodic_task_tenant_links', to='client.client'),
        ),
        migrations.AddField(
            model_name='client',
            name='available_features',
            field=models.ManyToManyField(blank=True, null=True, to='client.softwarefeatures'),
        ),
    ]