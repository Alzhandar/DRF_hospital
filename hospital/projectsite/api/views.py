from django.shortcuts import render
from rest_framework import viewsets, mixins, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Doctor, Patient, Visit, Service
from api.serializers import *
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from api.permissions import DoctorAccessPermission, RoleBasedPermissionsMixin, HasPermissionOrAuthenticatedUserRole
import django_filters.rest_framework
from django_filters.rest_framework import DjangoFilterBackend
from api.filters import DoctorFilterset
from rest_framework.filters import SearchFilter
from api.service import get_upcoming_visits_count
from rest_framework import status
from django.contrib.auth.models import User
# Create your views here.

class HospitalGenericViewSet(RoleBasedPermissionsMixin, viewsets.GenericViewSet):
    permission_classes = [HasPermissionOrAuthenticatedUserRole,]

class DoctorView(HospitalGenericViewSet,
                 RoleBasedPermissionsMixin,
                 viewsets.GenericViewSet,
                 mixins.ListModelMixin,
                 mixins.UpdateModelMixin,
                 mixins.RetrieveModelMixin,
                 mixins.CreateModelMixin,
                 mixins.DestroyModelMixin):
    
    lookup_field='id'

    filter_backends=[DjangoFilterBackend]
    filterset_fields=['first_name','last_name','specialization']
    filter_class=DoctorFilterset
    permission_classes=[IsAuthenticated,HasPermissionOrAuthenticatedUserRole]
    # permission_classes=[IsAuthenticated,DoctorAccessPermission]
    authentication_classes=[TokenAuthentication]

    def get_action_permissions(self):
        self.action_permissions = [] 
        if self.action in ('list','retrieve'):
            self.action_permissions=['view_doctor',]
        elif self.action=='list_patient':
            self.action_permissions=['view_patient',]

    def get_serializer_class(self):
        if self.action == 'list':
            return DoctorListSerializer
        if self.action == 'retrieve':
            return DoctorRetrieveSerializer
        if self.action == 'create':
            return DoctorCreateSerializer
        if self.action == 'update':
            return DoctorUpdateSerializer
        if self.action == 'list_patient':
            return PatientListSerializer
        else:
            return None
     
    
    def get_queryset(self):
        if self.action=='list_patient':
            return Patient.objects.prefetch_related(
                'visits'
            ).all()
        return Doctor.objects.all()
    
    def list_patient(self,request,id):
        queryset=self.get_queryset().filter(visits__doctor_id=id)
        serializer=self.get_serializer(queryset,many=True)
        return Response(data=serializer.data)
    

class ServiceViewSet(
                     viewsets.GenericViewSet, 
                     mixins.ListModelMixin, 
                     mixins.CreateModelMixin, 
                     mixins.RetrieveModelMixin, 
                     mixins.UpdateModelMixin, 
                     mixins.DestroyModelMixin):
    queryset = Service.objects.all()
    serializer_class = ServiceSerializer


class VisitViewSet(viewsets.GenericViewSet, 
                   mixins.ListModelMixin, 
                   mixins.CreateModelMixin, 
                   mixins.RetrieveModelMixin, 
                   mixins.UpdateModelMixin, 
                   mixins.DestroyModelMixin):
    queryset = Visit.objects.all()
    serializer_class = VisitSerializer

class DoctorViewSet(viewsets.GenericViewSet, 
                    mixins.ListModelMixin, 
                    mixins.CreateModelMixin, 
                    mixins.RetrieveModelMixin, 
                    mixins.UpdateModelMixin, 
                    mixins.DestroyModelMixin):
    queryset = Doctor.objects.all()
    serializer_class = DoctorListSerializer

    @action(detail=True, methods=['get'], url_path='list-patients')
    def list_patients(self, request, pk=None):
        doctor = self.get_object()
        patients = Patient.objects.filter(visit__doctor=doctor)
        serializer = PatientListSerializer(patients, many=True)
        return Response(serializer.data)
    
class PatientViewSet(viewsets.GenericViewSet, 
                     mixins.ListModelMixin, 
                     mixins.CreateModelMixin, 
                     mixins.RetrieveModelMixin, 
                     mixins.UpdateModelMixin, 
                     mixins.DestroyModelMixin):
    
    queryset = Patient.objects.all()
    filter_backends = [DjangoFilterBackend,]
    filterset_fields = ['gender']
    search_field=['first_name','last_name']
    
    def get_action_permissions(self):
        if self.action in ('list', 'retrieve'):
            self.action_permissions = ['view_patient',]
        elif self.action == 'create':
            self.action_permissions = ['add_patient',]
        elif self.action == 'update':
            self.action_permissions=['change_patient']
        elif self.action == 'destroy':
            self.action_permissions = ['delete_patient']
        else:
            self.action_permissions = []

    def get_serializer_class(self):
        if self.action == 'list':
            return PatientListSerializer
        elif self.action == 'retrieve':
            return PatientDetailedSerializer
        elif self.action in ['create', 'update']:
            return PatientCreateOrUpdateSerializer
        

class VisitView(viewsets.GenericViewSet, 
                     mixins.ListModelMixin, 
                     mixins.CreateModelMixin, 
                     mixins.RetrieveModelMixin, 
                     mixins.UpdateModelMixin, 
                     mixins.DestroyModelMixin):
    
    
    lookup_field='id'
    
    def get_action_permissions(self):
        if self.action in ('list', 'retrieve'):
            self.action_permissions = ['view_visit',]
        elif self.action == 'create':
            self.action_permissions = ['add_visit',]
        # elif self.action == 'update':
        #     self.action_permissions=['change_visit']
        # elif self.action == 'destroy':
        #     self.action_permissions = ['delete_visit']
        else:
            self.action_permissions = []

    def get_serializer_class(self):
        if self.action == 'list':
            return PatientListSerializer
        elif self.action == 'retrieve':
            return PatientDetailedSerializer
        elif self.action in ['create']:
            return VisitCreateSerializer
        elif self.action == 'update':
            return PatientCreateOrUpdateSerializer
        
    def get_queryset(self):
        return Visit.objects.all()


class AnalyticsView(HospitalGenericViewSet):

    def get_action_permissions(self):
        if self.action == "get_analytics":
            self.action_permissions = []

    @action(detail=False, methods=['get'])
    def get_analytics(self, request):
        response = {
            'patient_count': Patient.objects.count(),  
            'doctor_count': Doctor.objects.count(), 
            'visit_count': get_upcoming_visits_count()
        }
        return Response(response, status=status.HTTP_200_OK)
    

class FinancialRecordViewSet(viewsets.ModelViewSet):
    queryset = FinancialRecord.objects.all()
    serializer_class = FinancialRecordSerializer

class PatientSatisfactionViewSet(viewsets.ModelViewSet):
    queryset = PatientSatisfaction.objects.all()
    serializer_class = PatientSatisfactionSerializer
