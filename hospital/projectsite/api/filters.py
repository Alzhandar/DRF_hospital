import django_filters as filters
from api.models import *

class DoctorFilterset(filters.FilterSet):
    last_name=filters.CharFilter()

    class Meta:
        model=Doctor
        fields={
            'last_name':['exact','icontains']
        }