from django.contrib import admin
from django import forms
from .models import Patient, Doctor, Appointment

@admin.register(Patient)
class PatientAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'email', 'phone_number', 'date_of_birth')
    search_fields = ('first_name', 'last_name', 'email')
    list_filter = ('date_of_birth',)

@admin.register(Doctor)
class DoctorAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'specialty', 'email', 'phone_number')
    search_fields = ('first_name', 'last_name', 'specialty')
    list_filter = ('specialty',)

@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = ('patient', 'doctor', 'start_time', 'end_time', 'status', 'is_past_appointment')
    list_filter = ('status', 'doctor', 'start_time')
    search_fields = ('patient__first_name', 'patient__last_name', 'doctor__first_name', 'doctor__last_name', 'notes')
    date_hierarchy = 'start_time'
    raw_id_fields = ('patient', 'doctor') # Mejora la UX para seleccionar FKs con muchos objetos

    fieldsets = (
        (None, {
            'fields': ('patient', 'doctor', 'start_time', 'end_time', 'status')
        }),
        ('Información Adicional', {
            'fields': ('notes',),
            'classes': ('collapse',)
        }),
    )