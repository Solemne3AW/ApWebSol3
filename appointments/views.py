from django.shortcuts import render, get_object_or_404, redirect
from django.core.exceptions import ValidationError
from django.http import HttpResponse, JsonResponse
from django.views.decorators.http import require_http_methods
from django.forms.models import model_to_dict
from .models import Patient, Doctor, Appointment
from .forms import AppointmentForm # Crearemos este formulario en el siguiente paso

# Vistas para Pacientes
def patient_list(request):
    patients = Patient.objects.all()
    return render(request, 'appointments/patient_list.html', {'patients': patients})

def patient_detail(request, pk):
    patient = get_object_or_404(Patient, pk=pk)
    return render(request, 'appointments/patient_detail.html', {'patient': patient})

# Vistas para Citas
def appointment_list(request):
    # Consultas y Filtros: Filtrar por estado, médico, o fecha
    status = request.GET.get('status')
    doctor_id = request.GET.get('doctor')
    date_str = request.GET.get('date')

    appointments = Appointment.objects.all()

    if status:
        appointments = appointments.filter(status=status)
    if doctor_id:
        appointments = appointments.filter(doctor__id=doctor_id)
    if date_str:
        try:
            from datetime import datetime
            date_obj = datetime.strptime(date_str, '%Y-%m-%d').date()
            appointments = appointments.filter(start_time__date=date_obj)
        except ValueError:
            pass # Manejar error de formato de fecha

    appointments = appointments.order_by('start_time')
    doctors = Doctor.objects.all()
    statuses = Appointment.STATUS_CHOICES

    return render(request, 'appointments/appointment_list.html', {
        'appointments': appointments, 
        'doctors': doctors,
        'statuses': statuses,
        })

def appointment_create(request):
    if request.method == 'POST':
        form = AppointmentForm(request.POST)
        try:
            if form.is_valid():
                form.save()
                return redirect('appointments:appointment_list')
        except ValidationError as e:
            form.add_error(None, e) 
            for field, messages in e.message_dict.items():
                for message in messages:
                    form.add_error(field, message)
    else:
        form = AppointmentForm()
    
    return render(request, 'appointments/appointment_form.html', {'form': form})

def appointment_update(request, pk):
    appointment = get_object_or_404(Appointment, pk=pk)
    if request.method == 'POST':
        form = AppointmentForm(request.POST, instance=appointment)
        if form.is_valid():
            form.save()
            return redirect('appointments:appointment_list')
    else:
        form = AppointmentForm(instance=appointment)
    return render(request, 'appointments/appointment_form.html', {'form': form})

def appointment_delete(request, pk):
    appointment = get_object_or_404(Appointment, pk=pk)
    if request.method == 'POST':
        appointment.delete()
        return redirect('appointments:appointment_list')
    return render(request, 'appointments/appointment_confirm_delete.html', {'appointment': appointment})

@require_http_methods(["POST"])
def appointment_change_status(request, pk):
    appointment = get_object_or_404(Appointment, pk=pk)
    new_status = request.POST.get('status')

    if new_status in [choice[0] for choice in Appointment.STATUS_CHOICES]:
        appointment.status = new_status
        appointment.save()
        return JsonResponse({'status': 'success', 'new_status': new_status})
    return JsonResponse({'status': 'error', 'message': 'Invalid status'}, status=400)
