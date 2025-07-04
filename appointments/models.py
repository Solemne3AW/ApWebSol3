from django.db import models
from django.utils import timezone
from datetime import timedelta
from django.core.exceptions import ValidationError

class Patient(models.Model):
    """
    Representa a un paciente en el sistema.
    """
    first_name = models.CharField(max_length=100, verbose_name="Nombre")
    last_name = models.CharField(max_length=100, verbose_name="Apellido")
    date_of_birth = models.DateField(verbose_name="Fecha de Nacimiento")
    phone_number = models.CharField(max_length=20, blank=True, null=True, verbose_name="Teléfono")
    email = models.EmailField(unique=True, verbose_name="Correo Electrónico")
    address = models.TextField(blank=True, null=True, verbose_name="Dirección")

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    class Meta:
        verbose_name = "Paciente"
        verbose_name_plural = "Pacientes"
        ordering = ['last_name', 'first_name']

class Doctor(models.Model):
    """
    Representa a un médico en el sistema.
    """
    first_name = models.CharField(max_length=100, verbose_name="Nombre")
    last_name = models.CharField(max_length=100, verbose_name="Apellido")
    specialty = models.CharField(max_length=100, verbose_name="Especialidad")
    phone_number = models.CharField(max_length=20, blank=True, null=True, verbose_name="Teléfono")
    email = models.EmailField(unique=True, verbose_name="Correo Electrónico")

    def __str__(self):
        return f"Dr. {self.first_name} {self.last_name} ({self.specialty})"

    class Meta:
        verbose_name = "Médico"
        verbose_name_plural = "Médicos"
        ordering = ['last_name', 'first_name']

class Appointment(models.Model):
    """
    Representa una cita médica.
    """
    STATUS_CHOICES = [
        ('scheduled', 'Agendada'),
        ('completed', 'Completada'),
        ('cancelled', 'Cancelada'),
        ('rescheduled', 'Reagendada'),
    ]

    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='appointments', verbose_name="Paciente")
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, related_name='appointments', verbose_name="Médico")
    start_time = models.DateTimeField(verbose_name="Hora de Inicio")
    end_time = models.DateTimeField(verbose_name="Hora de Fin")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='scheduled', verbose_name="Estado")
    notes = models.TextField(blank=True, null=True, verbose_name="Motivo")

    def __str__(self):
        return f"Cita de {self.patient} con {self.doctor} el {self.start_time.strftime('%Y-%m-%d %H:%M')}"

    class Meta:
        verbose_name = "Cita"
        verbose_name_plural = "Citas"
        ordering = ['start_time']
        unique_together = ('doctor', 'start_time') # Un médico no puede tener dos citas a la misma hora

    # Lógica de Negocio: Validaciones y Métodos

    def clean(self):
        super().clean()  # Llama al método clean del padre
        if self.start_time and self.end_time:
            # Validar que la hora de fin sea posterior a la de inicio
            if self.start_time >= self.end_time:
                raise ValidationError("La hora de fin debe ser posterior a la hora de inicio.")
            # Validar que no se agende en el pasado
            if self.start_time < timezone.now():
                raise ValidationError("No se puede agendar una cita en el pasado.")
            # Validar duración mínima de 15 minutos
            if self.end_time - self.start_time < timedelta(minutes=15):
                raise ValidationError("La duración mínima de la cita es de 15 minutos.")
            # Validar superposición de citas
            if self.doctor and self.start_time and self.end_time:
                overlapping_appointments = Appointment.objects.filter(
                    doctor=self.doctor,
                    start_time__lt=self.end_time,
                    end_time__gt=self.start_time
                ).exclude(pk=self.pk if self.pk else None)
                if overlapping_appointments.exists():
                    raise ValidationError("El médico ya tiene una cita agendada que se superpone con este horario.")
                
    def save(self, *args, **kwargs):
        self.full_clean() # Llama a clean() antes de guardar
        super().save(*args, **kwargs)

    def is_past_appointment(self):
        """
        Verifica si la cita ya ha pasado.
        """
        return self.end_time < timezone.now()
    is_past_appointment.admin_order_field = 'end_time'
    is_past_appointment.boolean = True
    is_past_appointment.short_description = 'Cita Pasada?'

    def get_duration(self):
        """
        Calcula la duración de la cita.
        """
        return self.end_time - self.start_time