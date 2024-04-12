from django.contrib import admin
from .models import *


@admin.register(Specialization)
class SpecializationAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
    search_fields = ('name',)

@admin.register(Doctor)
class DoctorAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'specialization', 'contact_info')
    list_filter = ('specialization',)
    search_fields = ('first_name', 'last_name')

@admin.register(Patient)
class PatientAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'date_of_birth', 'gender', 'contact_info')
    list_filter = ('gender',)
    search_fields = ('first_name', 'last_name')

@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'cost')
    search_fields = ('name',)

@admin.register(Visit)
class VisitAdmin(admin.ModelAdmin):
    list_display = ('doctor', 'patient', 'service', 'visit_date_time', 'status')
    list_filter = ('status', 'doctor', 'patient')
    search_fields = ('doctor__first_name', 'doctor__last_name', 'patient__first_name', 'patient__last_name')

admin.site.register(Schedule)