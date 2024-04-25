from rest_framework import serializers
from .models import CompanyInfo

class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = CompanyInfo
        fields = '__all__'
    
        