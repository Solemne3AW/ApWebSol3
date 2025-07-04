from django.urls import path
from . import views

app_name = 'appointments'

urlpatterns = [
    # URLs para Pacientes
    path('patients/', views.patient_list, name='patient_list'),
    path('patients/<int:pk>/', views.patient_detail, name='patient_detail'),

    # URLs para Citas
    path('', views.appointment_list, name='appointment_list'),
    path('create/', views.appointment_create, name='appointment_create'),
    path('<int:pk>/update/', views.appointment_update, name='appointment_update'),
    path('<int:pk>/delete/', views.appointment_delete, name='appointment_delete'),
]