from rest_framework import status, permissions
from .models import CompanyInfo
from .serializers import CompanySerializer
from staff.serializers import *
from staff.models import *
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes

@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def get_companies(request):
    try:
        faculties = StaffUser.objects.filter(role='2')
        serialized_data = StaffUserSerializer(faculties, many=True)
        updated_data = []
        for user_data in serialized_data.data:
            user_id = user_data['id']
            professional_data = ProfessionalDetailsInfo.objects.filter(user=user_id)
            professional_serializer = ProfessionalDetailsInfoSerializer(professional_data, many=True)

            project_data = ProjectDetailsInfo.objects.filter(user=user_id)
            project_serializer = ProjectDetailsInfoSerializer(project_data, many=True)

            certificate_data = CertificateInfo.objects.filter(user=user_id)
            certificate_serializer = CertificateInfoSerializer(certificate_data, many=True)

            education_data = EducationInfo.objects.filter(user=user_id)
            education_serializer = EducationInfoSerializer(education_data, many=True)

            pricing_data = PricingInfo.objects.filter(user=user_id)
            pricing_serializer = PricingInfoSerializer(pricing_data, many=True)

            user_data['professional_details_info'] = professional_serializer.data
            user_data['project_details_info'] = project_serializer.data
            user_data['certificate_info'] = certificate_serializer.data
            user_data['education_info'] = education_serializer.data
            user_data['pricing_info'] = pricing_serializer.data
            updated_data.append(user_data)
        return Response({'companies': updated_data}, status=200)
    except Exception as e:
        return Response({'error': str(e)}, status=500)
