from django.contrib import admin
from django.urls import path
from .views import *
# from rest_framework.authtoken.views import obtain_auth_token
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView


urlpatterns = [
    path('doctor/', DoctorView.as_view({'get': 'list', 'post': 'create'})),
    path('doctor/<int:id>', DoctorView.as_view({'get': 'retrieve', 'put': 'update','delete':'destroy'})),
    path('doctor/<int:id>/patient/',DoctorView.as_view({'get':'list_patient'})),
    # path('token/',obtain_auth_token),
    path('token/',TokenObtainPairView.as_view(),name='token_obtain_pair'),
    path('token/refresh/',TokenRefreshView.as_view(),name='token_refresh'),
    path('patient/', PatientViewSet.as_view({'get': 'list', 'post': 'create'})),
    path('patient/<int:id>', PatientViewSet.as_view({'get': 'retrieve', 'put': 'update','delete':'destroy'})),
    path('visit/',VisitView.as_view({'post' : 'create'})),
    path('analytics/', AnalyticsView.as_view({'get': 'get_analytics'}), name='analytics'),
        path('financial_records/', FinancialRecordViewSet.as_view({
        'get': 'list',
        'post': 'create'
    }), name='financial_records'),
    path('financial_records/<int:pk>/', FinancialRecordViewSet.as_view({
        'get': 'retrieve',
        'put': 'update',
        'delete': 'destroy'
    }), name='financial_record_detail'),
    path('patient_satisfaction/', PatientSatisfactionViewSet.as_view({
        'get': 'list',
        'post': 'create'
    }), name='patient_satisfaction'),
    path('patient_satisfaction/<int:pk>/', PatientSatisfactionViewSet.as_view({
        'get': 'retrieve',
        'put': 'update',
        'delete': 'destroy'
    }), name='patient_satisfaction_detail'),


]
