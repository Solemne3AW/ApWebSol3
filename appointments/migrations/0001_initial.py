# Generated by Django 5.2.3 on 2025-07-04 00:19

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Doctor',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=100, verbose_name='Nombre')),
                ('last_name', models.CharField(max_length=100, verbose_name='Apellido')),
                ('specialty', models.CharField(max_length=100, verbose_name='Especialidad')),
                ('phone_number', models.CharField(blank=True, max_length=20, null=True, verbose_name='Teléfono')),
                ('email', models.EmailField(max_length=254, unique=True, verbose_name='Correo Electrónico')),
            ],
            options={
                'verbose_name': 'Médico',
                'verbose_name_plural': 'Médicos',
                'ordering': ['last_name', 'first_name'],
            },
        ),
        migrations.CreateModel(
            name='Patient',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=100, verbose_name='Nombre')),
                ('last_name', models.CharField(max_length=100, verbose_name='Apellido')),
                ('date_of_birth', models.DateField(verbose_name='Fecha de Nacimiento')),
                ('phone_number', models.CharField(blank=True, max_length=20, null=True, verbose_name='Teléfono')),
                ('email', models.EmailField(max_length=254, unique=True, verbose_name='Correo Electrónico')),
                ('address', models.TextField(blank=True, null=True, verbose_name='Dirección')),
            ],
            options={
                'verbose_name': 'Paciente',
                'verbose_name_plural': 'Pacientes',
                'ordering': ['last_name', 'first_name'],
            },
        ),
        migrations.CreateModel(
            name='Appointment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start_time', models.DateTimeField(verbose_name='Hora de Inicio')),
                ('end_time', models.DateTimeField(verbose_name='Hora de Fin')),
                ('status', models.CharField(choices=[('scheduled', 'Agendada'), ('completed', 'Completada'), ('cancelled', 'Cancelada'), ('rescheduled', 'Reagendada')], default='scheduled', max_length=20, verbose_name='Estado')),
                ('notes', models.TextField(blank=True, null=True, verbose_name='Motivo')),
                ('doctor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='appointments', to='appointments.doctor', verbose_name='Médico')),
                ('patient', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='appointments', to='appointments.patient', verbose_name='Paciente')),
            ],
            options={
                'verbose_name': 'Cita',
                'verbose_name_plural': 'Citas',
                'ordering': ['start_time'],
                'unique_together': {('doctor', 'start_time')},
            },
        ),
    ]
