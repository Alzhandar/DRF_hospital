from rest_framework import serializers
from .models import *
from rest_framework.exceptions import ValidationError

class DoctorListSerializer(serializers.Serializer):
    full_name = serializers.CharField()
    contact_info = serializers.CharField()

class DoctorRetrieveSerializer(serializers.ModelSerializer):
    class Meta:
        model = Doctor
        fields = '__all__'

class DoctorCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Doctor
        fields = '__all__'

class DoctorUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Doctor
        fields = ['specialization', 'contact_info']

class PatientListSerializer(serializers.Serializer):
    id=serializers.IntegerField()
    full_name = serializers.CharField()
    date_of_birth = serializers.DateField()
    gender = serializers.CharField()

class ServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Service
        fields = '__all__'
    
class VisitSerializer(serializers.ModelSerializer):
    class Meta:
        model = Visit
        fields = '__all__'

class PatientDetailedSerializer(PatientListSerializer):
    contact_info = serializers.CharField()

class PatientCreateOrUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Patient
        fields = '__all__'


class VisitCreateSerializer(serializers.ModelSerializer):
    def validate_schedule(self, value):
        visit_count = value.visits.count()
        if value.max_count <= visit_count:
            raise ValidationError('Количество мест ограничено.')
        return value  
    class Meta:
        model = Visit
        fields = ('patient',  'service', 'schedule')


class ScheduleSerializer(serializers.ModelSerializer):
    def validate(self, attrs):
        attrs = super().validate(attrs)
        timestamp_start, timestamp_end = attrs['timestamp_start'], attrs['timestamp_end']
        exists = Schedule.objects.filter(
            timestamp_start__lte=timestamp_start,
            timestamp_end__gte=timestamp_start
        ).exists()
        if exists:
            raise ValidationError("У нас уже есть запись на этот временной промежуток.")
        return attrs

    class Meta:
        model = Schedule
        fields = '__all__'


class FinancialRecordSerializer(serializers.ModelSerializer):
    class Meta:
        model = FinancialRecord
        fields = '__all__'

class PatientSatisfactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = PatientSatisfaction
        fields = '__all__'