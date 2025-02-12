# Generated by Django 5.1.3 on 2025-01-19 08:39

import datetime
import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dental_plan', '0008_patienttreatment_is_completed'),
        ('dental_structure', '0003_alter_dentaldiagnosisprocedures_dental_service_type_and_more'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.RemoveField(
            model_name='patienttreatment',
            name='created_by',
        ),
        migrations.RemoveField(
            model_name='patienttreatment',
            name='treatment',
        ),
        migrations.RemoveField(
            model_name='payment',
            name='patient_treatment',
        ),
        migrations.RemoveField(
            model_name='payment',
            name='created_by',
        ),
        migrations.AddField(
            model_name='treatmentmaterialused',
            name='amount',
            field=models.DecimalField(decimal_places=2, default=10.0, max_digits=10),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='treatmentmaterialused',
            name='discount_amount',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=10),
        ),
        migrations.AddField(
            model_name='treatmentmaterialused',
            name='discounted_amount',
            field=models.DecimalField(decimal_places=2, default=10.0, editable=False, max_digits=10),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='treatmentmaterialused',
            name='notes',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='treatmentmaterialused',
            name='payment_date',
            field=models.DateField(default=datetime.datetime(2025, 1, 19, 8, 39, 18, 721373, tzinfo=datetime.timezone.utc)),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='treatmentmaterialused',
            name='payment_method',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='treatmentmaterialused',
            name='payment_status',
            field=models.CharField(choices=[('Pending', 'Pending'), ('Completed', 'Completed'), ('Failed', 'Failed')], default='Pending', max_length=20),
        ),
        migrations.AddField(
            model_name='treatmentmaterialused',
            name='total_amount',
            field=models.DecimalField(decimal_places=2, default=10.0, editable=False, max_digits=10),
            preserve_default=False,
        ),
        migrations.CreateModel(
            name='CompanyTreatmentProcedures',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('last_modified_date', models.DateTimeField(auto_now=True)),
                ('deleted_at', models.DateTimeField(blank=True, null=True)),
                ('procedure_name', models.CharField(blank=True, max_length=255, null=True)),
                ('service_type_name', models.CharField(blank=True, max_length=255, null=True)),
                ('price', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('created_by', models.ForeignKey(default=None, editable=False, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='%(class)s_createdby', to=settings.AUTH_USER_MODEL)),
                ('procedure_id', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='dental_structure.dentaltreatmentprocedures')),
                ('service_type_id', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='dental_structure.dentaltreatmenttypes')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='CompanyTreamentProcedureSession',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('last_modified_date', models.DateTimeField(auto_now=True)),
                ('deleted_at', models.DateTimeField(blank=True, null=True)),
                ('session_name', models.CharField(blank=True, max_length=255, null=True)),
                ('session_duration', models.CharField(blank=True, max_length=255, null=True)),
                ('created_by', models.ForeignKey(default=None, editable=False, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='%(class)s_createdby', to=settings.AUTH_USER_MODEL)),
                ('company_treatment_procedures', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='dental_plan.companytreatmentprocedures')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AlterField(
            model_name='treatmentmaterialused',
            name='patient_treatment',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='payments', to='dental_plan.companytreatmentprocedures'),
        ),
        migrations.DeleteModel(
            name='DentalHistory',
        ),
        migrations.DeleteModel(
            name='Payment',
        ),
        migrations.DeleteModel(
            name='PatientTreatment',
        ),
    ]
