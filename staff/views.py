from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView
from django.contrib.auth.models import User
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status, permissions
from rest_framework.exceptions import NotFound
from .serializers import MyTokenObtainPairSerializer, StaffUserSerializer
from reservation.serializers import CandidateBlockSerializer
from company.serializers import CompanySerializer
from .serializers import *
from django.shortcuts import get_object_or_404
from .models import *
from reservation.models import BlockedCandidate
from company.models import CompanyInfo
from django.core.mail import send_mail
from datetime import datetime
from django.utils import timezone
from datetime import timedelta
from urllib.parse import urlparse, parse_qs
from django.core.exceptions import ObjectDoesNotExist,MultipleObjectsReturned
from django.core.mail import EmailMessage
from django.http import Http404
import hashlib
import jwt
from django.conf import settings
import random
import string
import base64 
import re
from django.http import JsonResponse
import razorpay
import os
from django.template.loader import render_to_string
from django.views.decorators.csrf import csrf_exempt

class ObtainTokenPairWithColorView(TokenObtainPairView):
    permission_classes = (permissions.AllowAny,)
    serializer_class = MyTokenObtainPairSerializer

class LogoutView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    def post(self, request):
        try:
            if not request.user.is_authenticated:
                raise ValueError("User not authenticated")
            refresh_token = RefreshToken.for_user(request.user)
            if not refresh_token:
                raise ValueError("Refresh token not found")
            refresh_token.blacklist()
            return Response({'message': 'Logout successful'}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)


# Forgot password send resetlink 
class ForgotPassword(APIView):
    permission_classes = (permissions.AllowAny,)
    def post(self, request):
        try:
            user_email = request.data.get('email')
            staff_data = StaffUser.objects.get(email=user_email)
            otp = ''.join([str(random.randint(0, 9)) for _ in range(6)])
            staff_data.otp = otp
            staff_data.save()
            subject = 'Reset Your Password'
            context = {'otp': otp}
            html_message = render_to_string('forgot.html', context)
            plain_message = f'Hello,\n\nYour OTP to reset your password is: {otp} \n\nIf you did not request this reset, please ignore this email.\n\nThank you!'
            from_email = 'connect@hirein5.com'
            to_email = user_email.lower()
            send_mail(
                subject,
                plain_message,
                from_email,
                [to_email],
                html_message=html_message 
            )
            return Response({'message': 'OTP sent successfully.'}, status=status.HTTP_200_OK)
        except StaffUser.DoesNotExist:
            return Response({'error': 'User not found.'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'error': 'Failed to send OTP.'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class UpdatePassword(APIView): 
    permission_classes = (permissions.AllowAny,)
    def post(self, request):
        otp = request.data.get('otp')
        email = request.data.get('email')
        reset_user = StaffUser.objects.get(email=email)
        if reset_user.otp == otp:
            return Response({'message': True}, status=200)
        else:
            return Response({'message': False}, status=200)

    def put(self, request):
        try:
            new_password = request.data.get('new_password')
            email = request.data.get('email')
            reset_user = StaffUser.objects.get(email=email)
            reset_user.set_password(new_password)
            reset_user.save()
            return Response({'message': "Password reset successfully."}, status=200)
        except StaffUser.DoesNotExist:
            return Response({'error': 'User not found.'}, status=status.HTTP_404_NOT_FOUND)
        
class PasswordUpdate(APIView):
    permission_classes = [permissions.IsAuthenticated]
    def post(self, request):
        email = request.data.get('email')
        new_password = request.data.get('new_password')
        try:
            staff_user = StaffUser.objects.get(email=email)
        except ObjectDoesNotExist:
            return Response({"message": "User not found"}, status=404)
        staff_user.set_password(new_password)
        staff_user.save()
        return Response({"message": "Password updated successfully"})
            
# <-------------------create staffuser ----------------------->

class StaffUserCreate(APIView):
    permission_classes = (permissions.AllowAny,)
    def post(self, request, *args, **kwargs):
        staff_serializer = StaffUserSerializer(data=request.data)
        #Convert the email lower case
        email = request.data['email'].lower()
        if StaffUser.objects.filter(email=email).exists():
            return Response({"error": "User already exists"}, status=status.HTTP_400_BAD_REQUEST)
        request.data['email'] = email

        if staff_serializer.is_valid():
            company_data = request.data.get('company')
            if company_data:
                company_serializer = CompanySerializer(data=company_data)
                if company_serializer.is_valid():
                    company_instance = company_serializer.save()
                else:
                    return Response(company_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
                
                staff_data = staff_serializer.validated_data
                staff_data['company'] = company_instance.id
            else:
                staff_data = staff_serializer.validated_data

            staff_instance = staff_serializer.create(staff_data)
            print(staff_instance.company)

            # Generate JWT token
            refresh = RefreshToken.for_user(staff_instance)
            access_token = str(refresh.access_token)
            # Customize the response data
            if staff_instance.role == '2':
                response_data = {
                    'id': staff_instance.id,
                    'first_name': staff_instance.first_name,
                    'email': staff_instance.email,
                    'username': staff_instance.username,
                    'phone': staff_instance.phone,
                    'title': staff_instance.title,
                    'linked_in': staff_instance.linked_in,
                    'role': staff_instance.role,
                    'company': staff_instance.company.id if staff_instance.company else None,
                    'access_token': access_token,
                }
                return Response(response_data, status=status.HTTP_201_CREATED)
            if staff_instance.role == '3':
                response_data = {
                    'id': staff_instance.id,
                    'first_name': staff_instance.first_name,
                    'email': staff_instance.email,
                    'username': staff_instance.username,
                    'phone': staff_instance.phone,
                    'title': staff_instance.title,
                    'linked_in': staff_instance.linked_in,
                    'role': staff_instance.role,
                    'access_token': access_token,
                    "email_verification": staff_instance.email_verification,
                    "mobile_verification": staff_instance.mobile_verification,
                }
                return Response(response_data, status=status.HTTP_201_CREATED)
            
            if staff_instance.role in ['1', '4', '5']:
                response_data = {
                    'id': staff_instance.id,
                    'first_name': staff_instance.first_name,
                    'email': staff_instance.email,
                    'username': staff_instance.username,
                    'phone': staff_instance.phone,
                    'access_token': access_token,
                }
                return Response(response_data, status=status.HTTP_201_CREATED)
        return Response(staff_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

def mask_sensitive_info(data):
    # Mask email addresses
    # if 'email' in data and data['email'] is not None:
    #     data['email'] = re.sub(r'(?<=.{2}).(?=[^@]*?@)', '*', data['email'])

    if 'email' in data and data['email'] is not None:
        parts = data['email'].split('@')
        if len(parts) == 2:
            local_part = parts[0]
            domain_part = parts[1]
            if len(local_part) > 2:
                visible_part = local_part[:2] + '*' * (len(local_part) - 3) + local_part[-1]
                data['email'] = visible_part + '@' + domain_part

    # Mask usernames
    # if 'username' in data and data['username'] is not None:
    #     data['username'] = re.sub(r'(?<=.{2}).(?=[^@]*?@)', '*', data['username'])
    if 'username' in data and data['username'] is not None:
        parts = data['username'].split('@')
        if len(parts) == 2:
            local_part = parts[0]
            domain_part = parts[1]
            if len(local_part) > 2:
                visible_part = local_part[:2] + '*' * (len(local_part) - 3) + local_part[-1]
                data['username'] = visible_part + '@' + domain_part
        
    # Mask phone numbers
    if 'phone' in data and data['phone'] is not None:
        data['phone'] = re.sub(r'(\d{2})\d+(\d{2})', r'\1******\2', data['phone'])

    if 'passport_info' in data and data['passport_info'] is not None:
        number = data['passport_info']['passport_number']
        masked_number = re.sub(r'(?<=^\d{2})\d+(?=\d{2}$)', r'******', number)
        data['passport_info']['passport_number'] = masked_number

    if 'kyc_info' in data and data['kyc_info'] is not None:
        if 'aadhar_number' in data['kyc_info'] and data['kyc_info']['aadhar_number'] is not None:
            number = data['kyc_info']['aadhar_number']
            masked_number = re.sub(r'(?<=^\d{2})\d+(?=\d{2}$)', r'******', number)
            data['kyc_info']['aadhar_number'] = masked_number

        if 'pan_number' in data['kyc_info'] and data['kyc_info']['pan_number'] is not None:
            number = data['kyc_info']['pan_number']
            masked_number = re.sub(r'(?<=^\w{2})\w+(?=\w{2}$)', r'******', number)
            data['kyc_info']['pan_number'] = masked_number
    return data

# <---------------------get all staffusers ------------------------> 
    
@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])

def getUserDetailInBulk(request, user_id):
        recently_visited_profiles = request.data["users_list"] 
        blocked_candidate = BlockedCandidate.objects.all()
        # filter by Professional details
        try:
            professional_data = ProfessionalDetailsInfo.objects.filter(user=user_id)
            professional_serializer = ProfessionalDetailsInfoSerializer(professional_data, many=True)
        except ObjectDoesNotExist:
            return Response({"message": "Professional Details User not found"}, status=404)
        
        #filter by Project details
        try:
            Project_details_data = ProjectDetailsInfo.objects.filter(user=user_id)
            Project_details_serializer = ProjectDetailsInfoSerializer(Project_details_data, many=True)
        except ObjectDoesNotExist:
            return Response({"message": "Project Details User not found"}, status=404)
        
        #filter by education
        try:
            education_data = EducationInfo.objects.filter(user=user_id)
            education_serializer = EducationInfoSerializer(education_data, many=True)
        except ObjectDoesNotExist:
            return Response({"message": "Education Info User not found"}, status=404)
        
        #filter by Certificate details
        try:
            certification_data = CertificateInfo.objects.filter(user=user_id)
            certification_serializer = CertificateInfoSerializer(certification_data, many=True)
        except ObjectDoesNotExist:
            return Response({"message": "Certificate Info User not found"}, status=404)

        #filter by pricing details
        try:
            pricing_data = PricingInfo.objects.filter(user=user_id)
            pricing_serializer = PricingInfoSerializer(pricing_data, many=True)
        except ObjectDoesNotExist:
            return Response({"message": "Pricing Info User not found"}, status=404)
        #filter by interview details
        interview_data = InterviewInfo.objects.filter(user=user_id)
        interview_serializer = InterviewInfoSerializer(interview_data, many=True)
        try:
            interview_data = InterviewInfo.objects.filter(user=user_id)
            interview_serializer = InterviewInfoSerializer(interview_data, many=True)
            for interview in interview_serializer.data:
                if len(interview['candidate']) == 0:
                    interview['candidate']=None
                else: 
                    contract_candidate = interview['candidate']
                    staff_data = StaffUser.objects.filter(pk=contract_candidate)
                    serializer = StaffUserSerializer(staff_data, many=True)
                    interview['Candidate'] = serializer.data
        except Exception as e:
            return Response({'error': str(e)}, status=500)
        
        profiles = []  # Use a list to store multiple profiles
        for user_list in recently_visited_profiles:
            profile = StaffUser.objects.get(pk=user_list)
            candidate_blocked_instance= []
            for candidate in blocked_candidate:
                if candidate.candidate_id == user_list:
                    candidate_blocked_instance.append(candidate)
            if len(candidate_blocked_instance)!= 0:
                block_expiry = candidate_blocked_instance[0].expiry_date
            else:
                block_expiry = None

            interview_data = InterviewInfo.objects.filter(candidate=user_list)
            interview_status = False
            for interview_instance in interview_data:
                current_datetime = datetime.now()
                current_date = str(current_datetime.date())
                if interview_instance.date >= current_date:
                    interview_status = True
                    break
            serializer = StaffUserSerializer(profile)
            updated_user_data = serializer.data
            #masking
            updated_user_data = mask_sensitive_info(updated_user_data)
            
            updated_user_data['interview_status'] = interview_status
            updated_user_data['block_expiry'] = block_expiry
            updated_user_data['professional_details_info'] = professional_serializer.data
            updated_user_data['project_details_info'] = Project_details_serializer.data
            updated_user_data['education_info'] = education_serializer.data
            updated_user_data['certificate_info'] = certification_serializer.data
            updated_user_data['pricing_info'] = pricing_serializer.data
            updated_user_data['interview_info'] = interview_serializer.data
            profiles.append(updated_user_data)
        return Response(profiles, status=200)

# <---------------------------filter by role ------------------------------->

@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])       
def get_faculties(request):
    try:
        faculties = StaffUser.objects.filter(role='3')
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

            user_data['professional_details_info'] = professional_serializer.data
            user_data['project_details_info'] = project_serializer.data
            user_data['certificate_info'] = certificate_serializer.data
            user_data['education_info'] = education_serializer.data
            updated_data.append(user_data)
        return Response({'faculties': updated_data}, status=200)
    except Exception as e:
        return Response({'error': str(e)}, status=500)
    
@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def get_by_roles(request):
    if (request.method == 'GET'):
        try:
            admin_data = StaffUser.objects.filter(role__in=['1', '4', '5'])
            serializer = StaffUserSerializer(admin_data, many=True)
            return Response({'faculties': serializer.data}, status=200)
        except Exception as e:
            return Response({'error': str(e)}, status=500)

# <--------------------- Recently viewed Api ------------------->
    
@api_view(['GET', 'PUT', 'POST', 'DELETE'])
@permission_classes([permissions.IsAuthenticated])
def recently_visited(request, user_id):
    if (request.method == 'GET'):
        try:
            recently_visited_profiles = StaffUser.objects.filter(id = user_id).values('recently_visited')[0]
            return Response(recently_visited_profiles, status=200)
        except Exception as e:
            return Response({'error': str(e)}, status=500)
        
    if (request.method == "PUT"):
        try:
            new_entry = request.data["new_entry"]
            recently_visited_profiles = StaffUser.objects.filter(id = user_id).values('recently_visited')[0]["recently_visited"]
            if(new_entry not in recently_visited_profiles):
                recently_visited_profiles.append(new_entry)
                visited_update=StaffUser.objects.get(id = user_id)
                visited_update.recently_visited = recently_visited_profiles
                visited_update.save()
                recently_visited_profiles = StaffUser.objects.filter(id = user_id).values('recently_visited')[0]["recently_visited"]
            else: 
                pass
            return Response(recently_visited_profiles, status=200)
            
        except Exception as e:
            return Response({'error': str(e)}, status=500)
        
    if (request.method == "DELETE"):
        try:
            visited_update=StaffUser.objects.get(id = user_id)
            visited_update.recently_visited = []
            visited_update.save()
            return Response({}, status=200)
        
        except Exception as e:
            return Response({'error': str(e)}, status=500)

#--------------------add more(Contracts)--------------------------->
        
class Contracts(APIView):
    permission_classes = [permissions.IsAuthenticated]
    def post(self, request, user_id):
        contract_data = request.data.get('contracts_info', {})
        if contract_data:
            contract_data['user'] = user_id
            serializer = ContractsInfoSerializer(data=contract_data)
            if serializer.is_valid():
                contract_instance = ContractsInfo.objects.create(**contract_data)
                serialized_contract = ContractsInfoSerializer(contract_instance)
                return Response(serialized_contract.data, status=200)
            return Response(serializer.errors, status=400)

    def get(self, request, user_id):
        try:
            contracts_data = ContractsInfo.objects.filter(user=user_id)
            contract_serializer = ContractsInfoSerializer(contracts_data, many=True)
            for contract in contract_serializer.data:
                if len(contract['candidate']) == 0:
                    contract['candidate']=None
                else: 
                    contract_candidate = contract['candidate']
                    staff_data = StaffUser.objects.filter(pk=contract_candidate)
                    serializer = StaffUserSerializer(staff_data, many=True)
                    contract['Candidate'] = serializer.data
            return Response(contract_serializer.data, status=200)
        except Exception as e:
            return Response({'error': str(e)}, status=500)
        
    def put(self, request, user_id):
        try:
            contracts_instance = ContractsInfo.objects.get(pk=user_id)
            contracts_data = request.data.get('contracts_info', {})
            serializer = ContractsInfoSerializer(contracts_instance, data=contracts_data)
            if serializer.is_valid():
                contracts_instance = serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
                
        except ContractsInfo.DoesNotExist:
            return Response({'error': 'contracts_info not found'}, status=status.HTTP_404_NOT_FOUND)
        
    def delete(self, request, user_id):
        try:
            contract_instance = ContractsInfo.objects.get(candidate=user_id)
            contract_instance.delete()
            return Response({'message': 'Contract deleted successfully'}, status=status.HTTP_204_NO_CONTENT)
        except ContractsInfo.DoesNotExist:
            return Response({'error': 'Contract not found'}, status=status.HTTP_404_NOT_FOUND)


#--------------------add more(Interview)--------------------------->
        
class Interview(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, user_id):
        interview_data = request.data.get('interview_info', {})
        if interview_data:
            interview_data['user'] = user_id
            serializer = InterviewInfoSerializer(data=interview_data)
            if serializer.is_valid():
                interview_instance = InterviewInfo.objects.create(**interview_data)
                serialized_interview = InterviewInfoSerializer(interview_instance)
                return Response(serialized_interview.data, status=200)
            return Response(serializer.errors, status=400)

    def get(self, request, user_id):
        try:
            interview_data = InterviewInfo.objects.filter(user=user_id)
            interview_serializer = InterviewInfoSerializer(interview_data, many=True)
            for interview in interview_serializer.data:
                if len(interview['candidate']) == 0:
                    interview['candidate']=None
                else: 
                    interview_candidate = interview['candidate']
                    staff_data = StaffUser.objects.filter(pk=interview_candidate)
                    serializer = StaffUserSerializer(staff_data, many=True)
                    interview['Candidate'] = serializer.data
            return Response(interview_serializer.data, status=200)
        except Exception as e:
            return Response({'error': str(e)}, status=500)
        
    def put(self, request, user_id):
        try:
            interview_instance = InterviewInfo.objects.get(pk=user_id)
            interview_data = request.data.get('interview_info', {})
            serializer = InterviewInfoSerializer(interview_instance, data=interview_data)
            if serializer.is_valid():
                interview_instance = serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
                
        except InterviewInfo.DoesNotExist:
            return Response({'error': 'interview_info not found'}, status=status.HTTP_404_NOT_FOUND)
        

    def delete(self, request, user_id):
        try:
            instance = ContractsInfo.objects.get(candidate=user_id)
            instance.delete()
            return Response({'message': 'Contract deleted successfully'}, status=status.HTTP_204_NO_CONTENT)
        except ContractsInfo.DoesNotExist:
            return Response({'error': 'Contract not found'}, status=status.HTTP_404_NOT_FOUND)
#--------------------add more(ProffessionalDetails)--------------------------->
        
class ProffessionalDetails(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, user_id):
        professional_details_data = request.data.get('professional_details_info', {})
        if professional_details_data:
            professional_details_data['user'] = user_id
            serializer = ProfessionalDetailsInfoSerializer(data=professional_details_data)
            if serializer.is_valid():
                professional_details_instance = ProfessionalDetailsInfo.objects.create(**professional_details_data)
                serialized_details = ProfessionalDetailsInfoSerializer(professional_details_instance)
                return Response(serialized_details.data, status=200)
            return Response(serializer.errors, status=400)
    
    def get(self, request, user_id):
        try:
            professional_details_data = ProfessionalDetailsInfo.objects.filter(user=user_id)
            serializer = ProfessionalDetailsInfoSerializer(professional_details_data, many=True)
            return Response(serializer.data, status=200)
        except Exception as e:
            return Response({'error': str(e)}, status=500)
    
    def put(self, request, user_id):
        try:
            professional_details_instance = ProfessionalDetailsInfo.objects.get(pk=user_id)
            professional_details_data = request.data.get('professional_details_info', {})
            serializer = ProfessionalDetailsInfoSerializer(professional_details_instance, data=professional_details_data)
            if serializer.is_valid():
                professional_details_instance = serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
                
        except ProfessionalDetailsInfo.DoesNotExist:
            return Response({'error': 'ProfessionalDetailsInfo not found'}, status=status.HTTP_404_NOT_FOUND)

#--------------------add more(ProjectDetails)--------------------------->
        
class ProjectDetails(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, user_id):
        project_details_data = request.data.get('project_details_info', {})
        if project_details_data:
            project_details_data['user'] = user_id
            serializer = ProjectDetailsInfoSerializer(data=project_details_data)
            if serializer.is_valid():
                project_instance = ProjectDetailsInfo.objects.create(**project_details_data)
                serialized_data = ProjectDetailsInfoSerializer(project_instance)
                return Response(serialized_data.data, status=200)
            return Response(serializer.errors, status=400)
        
    def get(self, request, user_id):
        try:
            project_details_data = ProjectDetailsInfo.objects.filter(user=user_id)
            serializer = ProjectDetailsInfoSerializer(project_details_data, many=True)
            return Response(serializer.data, status=200)
        except Exception as e:
            return Response({'error': str(e)}, status=500)
        
    def put(self, request, user_id):
        try:
            project_details_instance = ProjectDetailsInfo.objects.get(pk=user_id)
            project_details_data = request.data.get('project_details_info', {})
            serializer = ProjectDetailsInfoSerializer(project_details_instance, data=project_details_data)
            if serializer.is_valid():
                project_details_instance = serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)      
        except ProjectDetailsInfo.DoesNotExist:
            return Response({'error': 'ProjectDetails not found'}, status=status.HTTP_404_NOT_FOUND)

#--------------------add more(Certifications)--------------------------->
        
class Certifications(APIView):
    permission_classes = [permissions.IsAuthenticated]
    def post(self, request, user_id):
        certification_data = request.data.get('certificate_info', {})
        if certification_data:
            certification_data['user'] = user_id
            serializer = CertificateInfoSerializer(data=certification_data)
            if serializer.is_valid():
                certification_instance = CertificateInfo.objects.create(**certification_data)
                serialized_data = CertificateInfoSerializer(certification_instance)
                return Response(serialized_data.data, status=200)
            return Response(serializer.errors, status=400)
        
    def get(self, request, user_id):
        try:
            certification_data = CertificateInfo.objects.filter(user=user_id)
            serializer = CertificateInfoSerializer(certification_data, many=True)
            return Response(serializer.data, status=200)
        except Exception as e:
            return Response({'error': str(e)}, status=500)
    
    def put(self, request, user_id):
        try:
            certification_instance = CertificateInfo.objects.get(pk=user_id)
            certification_data = request.data.get('certificate_info', {})
            serializer = CertificateInfoSerializer(certification_instance, data=certification_data)
            if serializer.is_valid():
                certification_instance = serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)      
        except CertificateInfo.DoesNotExist:
            return Response({'error': 'certificate_info not found'}, status=status.HTTP_404_NOT_FOUND)
        
#--------------------add more(Educations)--------------------------->
        
class Educations(APIView):
    permission_classes = [permissions.IsAuthenticated]
    def post(self, request, user_id):
        education_data = request.data.get('education_info', {})
        if education_data:
            education_data['user'] = user_id
            serializer = EducationInfoSerializer(data=education_data)
            if serializer.is_valid():
                education_instance = EducationInfo.objects.create(**education_data)
                serialized_data = EducationInfoSerializer(education_instance)
                return Response(serialized_data.data, status=200)
            return Response(serializer.errors, status=400)
        
    def get(self, request, user_id):
        try:
            education_data = EducationInfo.objects.filter(user=user_id)
            serializer = EducationInfoSerializer(education_data, many=True)
            return Response(serializer.data, status=200)
        except Exception as e:
            return Response({'error': str(e)}, status=500)
        
    def put(self, request, user_id):
        try:
            education_instance = EducationInfo.objects.get(pk=user_id)
            education_instance_data = request.data.get('education_info', {})
            serializer = EducationInfoSerializer(education_instance, data=education_instance_data)
            if serializer.is_valid():
                education_instance = serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)      
        except EducationInfo.DoesNotExist:
            return Response({'error': 'education_info not found'}, status=status.HTTP_404_NOT_FOUND)

#--------------------add more(pricing)--------------------------->

class PricingDetails(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, user_id):
        pricing_data = request.data.get('pricing_info', {})
        if pricing_data:
            pricing_data['user'] = user_id
            serializer = PricingInfoSerializer(data=pricing_data)
            if serializer.is_valid():
                pricing_instance = PricingInfo.objects.create(**pricing_data)
                serialized_pricing = PricingInfoSerializer(pricing_instance)
                return Response(serialized_pricing.data, status=200)
            return Response(serializer.errors, status=400)
    
    def get(self, request, user_id):
        try:
            pricing_data = PricingInfo.objects.filter(user=user_id)
            serializer = PricingInfoSerializer(pricing_data, many=True)
            return Response(serializer.data, status=200)
        except Exception as e:
            return Response({'error': str(e)}, status=500)
    
    def put(self, request, user_id):
        try:
            pricing_instance = PricingInfo.objects.get(pk=user_id)
            pricing_data = request.data.get('pricing_info', {})
            serializer = PricingInfoSerializer(pricing_instance, data=pricing_data)
            if serializer.is_valid():
                pricing_instance = serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)        
        except PricingInfo.DoesNotExist:
            return Response({'error': 'Pricing info not found'}, status=status.HTTP_404_NOT_FOUND)
    
    def delete(self, request, user_id):
        try:
            pricing_members = PricingInfo.objects.get(pk=user_id)
            pricing_members.delete()
            return Response({'message': 'Deleted Successfully'}, status=status.HTTP_204_NO_CONTENT)
        except PricingInfo.DoesNotExist:
            return Response({'error': 'teamMembers not found'}, status=status.HTTP_404_NOT_FOUND)

#--------------------add more(team_members)--------------------------->
        
@api_view(['GET', 'PUT', 'POST', 'DELETE'])
@permission_classes([permissions.IsAuthenticated])
def get_team_members(request, user_id):
    if request.method == 'POST':
        team_members_serializer = TeamMembersInfoSerializer(data=request.data)
        if team_members_serializer.is_valid():
            name = team_members_serializer.validated_data.get('name')
            email_id=team_members_serializer.validated_data.get('email_id')
            level_of_access=team_members_serializer.validated_data.get('level_of_access')
            status=team_members_serializer.validated_data.get('status')
            if email_id:
                env_url = os.environ.get('ENV_URL')
                subject = "Welcome to the Team"
                message = f"""URL: {env_url}/#/ Dear {name}, Welcome to our team! Your access level is {level_of_access}."""
                from_email = "connect@hirein5.com"
                to_email = email_id
                send_mail(subject, message, from_email, [to_email])
                team_members_data=TeamMembersInfo.objects.create(name=name, email_id=email_id, level_of_access=level_of_access, status=status)
                serialized_members = TeamMembersInfoSerializer(team_members_data)
            return Response(serialized_members.data, status=200)
        return Response(serialized_members.errors, status=400)

    if (request.method == 'GET'):
        try:
            team_members_data = TeamMembersInfo.objects.all()
            serializer = TeamMembersInfoSerializer(team_members_data, many=True)
            return Response(serializer.data, status=200)
        except Exception as e:
            return Response({'error': str(e)}, status=500) 
        
    if (request.method == 'PUT'):
        try:
            team_members_instance=TeamMembersInfo.objects.all()
            for team_members in team_members_instance:
                if team_members.id == user_id:
                    team_members_serializer = TeamMembersInfoSerializer(team_members, data=request.data)
                    if team_members_serializer.is_valid():
                        team_members_serializer.save()
                        return Response(team_members_serializer.data, status=200)
                    return Response(team_members_serializer.errors, status=400)
        except TeamMembersInfo.DoesNotExist:
            return Response({'error': 'Team Members not found'}, status=status.HTTP_404_NOT_FOUND)

    if (request.method == 'DELETE'):
        try:
            team_members = TeamMembersInfo.objects.get(id=user_id)
            team_members.delete()
            return Response({'message': 'Deleted Successfully'}, status=status.HTTP_204_NO_CONTENT)
        except TeamMembersInfo.DoesNotExist:
            return Response({'error': 'teamMembers not found'}, status=status.HTTP_404_NOT_FOUND) 

# <---------------------- filter by email to get staffuser data ------------------------->
@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def staff_data_by_email(request):
    if (request.method == 'GET'):
        try:
            email = request.data.get('email')
            staff_data = StaffUser.objects.get(email=email)
            serializer= StaffUserSerializer(staff_data, many=False)
            return Response({'staffUser_data': serializer.data}, status=200)
        except Exception as e:
            return Response({'error': str(e)}, status=500)

# <--------------------------Update staffuser data ----------------------------------->
      
class UpdateStaffUser(Contracts, ProffessionalDetails, ProjectDetails, Educations, Certifications, PricingDetails, Interview):
    permission_classes = [permissions.IsAuthenticated]
    queryset = StaffUser.objects.all()
    def get_object(self, user_id):
        try:
            return StaffUser.objects.get(pk=user_id)
        except StaffUser.DoesNotExist:
            raise NotFound(detail='User not found')

    def get(self, request, user_id):
        try:
            #filter by Professional details
            professional_data = ProfessionalDetailsInfo.objects.filter(user=user_id)
            professional_serializer = ProfessionalDetailsInfoSerializer(professional_data, many=True)
            #filter by Project details
            Project_details_data = ProjectDetailsInfo.objects.filter(user=user_id)
            Project_details_serializer = ProjectDetailsInfoSerializer(Project_details_data, many=True)
            #filter by education
            education_data = EducationInfo.objects.filter(user=user_id)
            education_serializer = EducationInfoSerializer(education_data, many=True)
            #filter by Project details
            certification_data = CertificateInfo.objects.filter(user=user_id)
            certification_serializer = CertificateInfoSerializer(certification_data, many=True)

            #filter by pricing details
            pricing_data = PricingInfo.objects.filter(user=user_id)
            pricing_serializer = PricingInfoSerializer(pricing_data, many=True)

            #filter by interview details
            interview_data = InterviewInfo.objects.filter(user=user_id)
            interview_serializer = InterviewInfoSerializer(interview_data, many=True)
            
            for interview in interview_serializer.data:
                if len(interview['candidate']) == 0:
                    interview['candidate'] = None
                else: 
                    contract_candidate = interview['candidate']
                    staff_data = StaffUser.objects.filter(pk=contract_candidate)
                    serializer = StaffUserSerializer(staff_data, many=True)
                    interview['candidate'] = serializer.data

            user_instance = self.get_object(user_id)
            blocked_candidate = BlockedCandidate.objects.all()
            candidate_blocked_instance= []
            for candidate in blocked_candidate:
                if candidate.candidate_id == user_id:
                    candidate_blocked_instance.append(candidate)
            if len(candidate_blocked_instance)!= 0:
                block_expiry = candidate_blocked_instance[0].expiry_date
            else:
                block_expiry = "null"
            serializer = StaffUserSerializer(user_instance)
            updated_user_data = serializer.data
            updated_user_data['block_expiry'] = block_expiry
            updated_user_data['professional_details_info'] = professional_serializer.data
            updated_user_data['project_details_info'] = Project_details_serializer.data
            updated_user_data['education_info'] = education_serializer.data
            updated_user_data['certificate_info'] = certification_serializer.data
            updated_user_data['pricing_info'] = pricing_serializer.data
            updated_user_data['interview_info'] = interview_serializer.data
            
            return Response(updated_user_data)

        except Exception as e:
            return Response({'error': str(e)}, status=500)
        
    def put(self, request, user_id, *args, **kwargs):
        try:
            user_instance = StaffUser.objects.get(pk=user_id)
            
        except StaffUser.DoesNotExist:
            return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
        
        user_serializer = StaffUserSerializer(user_instance, data=request.data)
        if user_serializer.is_valid():
            user_instance = user_serializer.save()

            if 'company' in request.data:
                company_instance = get_object_or_404(CompanyInfo, pk=user_instance.company.pk)
                company_serializer = CompanySerializer(company_instance, data=request.data['company'])
                if company_serializer.is_valid():
                    company_instance = company_serializer.save()
                    user_instance.company = company_instance
                else:
                    return Response(company_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

            # Update or create associated address information
            if 'address' in request.data:
                address_data = request.data['address']
                address_instance = user_instance.address
                address_serializer = AddressInfoSerializer(address_instance, data=address_data)
                if address_serializer.is_valid():
                    address_instance = address_serializer.save()
                    user_instance.address = address_instance
                else:
                    return Response(address_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
                
            # Update or create associated preference information
            if 'preference_info' in request.data:
                preference_data=request.data['preference_info']
                preference_instance=user_instance.preference_info
                preference_serializer = PreferenceSerializer(preference_instance, data=preference_data)
                if preference_serializer.is_valid():
                    preference_instance = preference_serializer.save()
                    user_instance.preference_info = preference_instance
                else:
                    return Response(PreferenceSerializer.errors, status=status.HTTP_400_BAD_REQUEST)
                
            if 'travel_info' in request.data:
                travelled_data=request.data['travel_info']
                travelled_instance=user_instance.travel_info
                travelled_serializer= TravelInfoSerializer(travelled_instance, data=travelled_data)
                if travelled_serializer.is_valid():
                    travelled_instance = travelled_serializer.save()
                    user_instance.travel_info = travelled_instance
                else:
                    return Response(TravelInfoSerializer.errors, status=status.HTTP_400_BAD_REQUEST)
                
            if 'work_preference_info' in request.data:
                work_preference_data = request.data['work_preference_info']
                work_preference_instance = user_instance.work_preference_info
                work_preference_serializer = WorkExperienceInfoSerializer(work_preference_instance, data=work_preference_data)
                if work_preference_serializer.is_valid():
                    work_preference_instance = work_preference_serializer.save()
                    user_instance.work_preference_info = work_preference_instance
                else:
                    return Response(work_preference_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
                
            if 'rate_card_info' in request.data:
                rate_card_data=request.data['rate_card_info']
                rate_card_instance=user_instance.rate_card_info
                rate_card_serializer=RateCardInfoSerializer(rate_card_instance, data=rate_card_data)
                if rate_card_serializer.is_valid():
                    rate_card_instance = rate_card_serializer.save()
                    user_instance.rate_card_info = rate_card_instance
                    
                else:
                    return Response(RateCardInfoSerializer.errors, status=status.HTTP_400_BAD_REQUEST)
                
            if 'passport_info' in request.data:
                passport_data=request.data['passport_info']
                passport_instance=user_instance.passport_info
                passport_serializer=PassportInfoSerializer(passport_instance, data=passport_data)
                if passport_serializer.is_valid():
                    passport_instance = passport_serializer.save()
                    user_instance.passport_info = passport_instance
                    
                else:
                    return Response(PassportInfoSerializer.errors, status=status.HTTP_400_BAD_REQUEST)
                
            if 'hire_info' in request.data:
                hire_data=request.data['hire_info']
                hire_instance=user_instance.hire_info
                hire_serializer=HireInfoSerializer(hire_instance, data=hire_data)
                if hire_serializer.is_valid():
                    hire_instance = hire_serializer.save()
                    user_instance.hire_info = hire_instance
                else:
                    return Response(HireInfoSerializer.errors, status=status.HTTP_400_BAD_REQUEST)
                
            if 'requirements_info' in request.data:
                requirements_info_data=request.data['requirements_info']
                requirements_info_instance=user_instance.requirements_info
                requirements_info_serializer=RequirementsInfoSerializer(requirements_info_instance, data=requirements_info_data)
                if requirements_info_serializer.is_valid():
                    requirements_info_instance = requirements_info_serializer.save()
                    user_instance.requirements_info = requirements_info_instance
                else:
                    return Response(RequirementsInfoSerializer.errors, status=status.HTTP_400_BAD_REQUEST)
                
            if 'contact_preference_info' in request.data:
                contact_preference_data=request.data['contact_preference_info']
                contact_preference_instance=user_instance.contact_preference_info
                contact_preference_serializer=ContactPreferenceSerializer(contact_preference_instance, data=contact_preference_data)
                if contact_preference_serializer.is_valid():
                    contact_preference_instance = contact_preference_serializer.save()
                    user_instance.contact_preference_info = contact_preference_instance
                else:
                    return Response(ContactPreferenceSerializer.errors, status=status.HTTP_400_BAD_REQUEST)
            
            # Serialize the updated user, company, and address data
            updated_user_data = user_serializer.data
            updated_company_data = CompanySerializer(company_instance).data if 'company' in request.data else None
            updated_address_data = AddressInfoSerializer(address_instance).data if 'address' in request.data else None
            updated_preference_data = PreferenceSerializer(preference_instance).data if 'preference_info' in request.data else None
            updated_travelled_data = TravelInfoSerializer(travelled_instance).data if 'travel_info' in request.data else None
            updated_work_preference_data = WorkExperienceInfoSerializer(work_preference_instance).data if 'work_preference_info' in request.data else None
            updated_passport_data = PassportInfoSerializer(passport_instance).data if 'passport_info' in request.data else None
            updated_hire_data = HireInfoSerializer(hire_instance).data if 'hire_info' in request.data else None
            updated_contact_preference_data = ContactPreferenceSerializer(contact_preference_instance).data if 'contact_preference_info' in request.data else None
            updated_requirements_data = RequirementsInfoSerializer(requirements_info_instance).data if 'requirements_info' in request.data else None
            
    
            updated_contracts_data = ContractsInfo.objects.filter(user=user_id)
            contracts_serializer = ContractsInfoSerializer(updated_contracts_data, many=True)

            updated_team_members_data = TeamMembersInfo.objects.filter(pk=user_id)
            team_members_serializer = TeamMembersInfoSerializer(updated_team_members_data, many=True)

            updated_professional_data = ProfessionalDetailsInfo.objects.filter(user=user_id)
            professional_serializer = ProjectDetailsInfoSerializer(updated_professional_data, many=True)

            updated_project_data = ProjectDetailsInfo.objects.filter(user=user_id)
            project_serializer = ProjectDetailsInfoSerializer(updated_project_data, many=True)

            updated_certificate_data = CertificateInfo.objects.filter(user=user_id)
            certificate_serializer = CertificateInfoSerializer(updated_certificate_data, many=True)

            updated_education_data = EducationInfo.objects.filter(user=user_id)
            education_serializer = EducationInfoSerializer(updated_education_data, many=True)

            updated_pricing_data = PricingInfo.objects.filter(user=user_id)
            pricing_serializer = PricingInfoSerializer(updated_pricing_data, many=True)

            updated_interview_data = InterviewInfo.objects.filter(user=user_id)
            interview_serializer = InterviewInfoSerializer(updated_interview_data, many=True)


            # Update user data with address and company
            updated_user_data['address'] = updated_address_data
            updated_user_data['company'] = updated_company_data
            updated_user_data['preference_info'] =  updated_preference_data
            updated_user_data['travel_info'] =  updated_travelled_data
            updated_user_data['work_preference_info'] =  updated_work_preference_data
            updated_user_data['passport_info'] =  updated_passport_data
            updated_user_data['hire_info'] =  updated_hire_data
            updated_user_data['contact_preference_info'] =  updated_contact_preference_data
            updated_user_data['requirements_info'] =  updated_requirements_data


            updated_user_data['contracts_info'] = contracts_serializer.data
            updated_user_data['team_members_info'] = team_members_serializer.data
            updated_user_data['professional_details_info'] = professional_serializer.data
            updated_user_data['project_details_info'] = project_serializer.data
            updated_user_data['certificate_info'] = certificate_serializer.data
            updated_user_data['education_info'] = education_serializer.data
            updated_user_data['pricing_info'] = pricing_serializer.data
            updated_user_data['interview_info'] = interview_serializer.data
            

            return Response({
                'message': 'User and Associated Info updated successfully',
                'user': updated_user_data,
            }, status=status.HTTP_200_OK)
        return Response(user_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, user_id):
        try:
            staff_user = StaffUser.objects.get(pk=user_id)
        except StaffUser.DoesNotExist:
            return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
        staff_user.delete()
        return Response({'message': 'User data deleted successfully'}, status=status.HTTP_204_NO_CONTENT)

#email validation   
class EmailVerification(APIView):
    permission_classes = (permissions.AllowAny,)
    @csrf_exempt
    def post(self, request, user_id):
        try:
           user_data = StaffUser.objects.get(pk=user_id)
        except StaffUser.DoesNotExist:
           return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)
        otp = ''.join([str(random.randint(0, 9)) for _ in range(6)])
        user_data.otp = otp
        user_data.save()
        serializer = StaffUserSerializer(user_data)
        serialized_data = serializer.data
        to_email = serialized_data.get('email')
        context = {'otp': otp} 
        subject = 'Verify your email address'
        html_message = render_to_string('email.html', context)
        plain_message = f"Before you sign in, we need to verify your identity. Enter the following code on the verification page: {otp}"
        from_email = 'connect@hirein5.com'  
        send_mail(
            subject,
            plain_message,
            from_email,
            [to_email],
            html_message=html_message   
        )
        return Response({"success": "OTP Sent Successfully!!!"}, status=status.HTTP_200_OK)

    def put(self, request, user_id):
        try:
            email = request.data.get('email')
            user_data = StaffUser.objects.get(email=email)
            otp = request.data.get('otp')
            if user_data.otp == otp:
                user_data.email_verification = True
                user_data.save()
                return Response({"message": "User data Updated Successfully!!!"}, status=status.HTTP_200_OK)
            else:
                user_data.email_verification = False
                user_data.save()
                return Response({"message": "The OTP entered is incorrect."}, status=status.HTTP_200_OK)
        except StaffUser.DoesNotExist:
            return Response({'error': 'User not Found.'}, status=status.HTTP_404_NOT_FOUND)           
        except Exception as e:
            return Response({'error': 'Internal Server Error'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

# <------------------------simple email notification -------------------------->
class EmailNotification(APIView):
    permission_classes = [permissions.IsAuthenticated]
    def post(self, request):
        try:
            user_email = request.data.get('email')
            subject = 'Verify your email address'
            from_email = 'connect@hirein5.com'  
            to_email = user_email.lower()
            plain_message = f"""URL:https://hirein5.netlify.app/#/adminsignUp/{user_email}"""
            send_mail(subject, plain_message, from_email, [to_email])
            return Response({"success": "Email Verification Link Sent Successfully!!!"}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
# <--------------------------Notification api -----------------------> 
class Notification(APIView):
    permission_classes = [permissions.IsAuthenticated]
    def post(self, request, user_id):
        message = request.data.get('message')
        status = request.data.get('status')
        on_type = request.data.get('on_type')
        request.data['user'] = user_id
        serializer = NotificationInfoSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        else:
            return Response(serializer.errors, status=400)
           
    def get(self, request, user_id):
        try:
            notifications_data = NotificationInfo.objects.all()
            serializer = NotificationInfoSerializer(notifications_data, many=True)
            return Response(serializer.data)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
     
    def put(self, request, user_id):
        try:
            notification_instance = NotificationInfo.objects.get(pk=user_id)
            notification_instance.status = "true"
            notification_instance.save()
            serializer = NotificationInfoSerializer(notification_instance)
            return Response(serializer.data)
        except NotificationInfo.DoesNotExist:
            return Response({'error': 'Notification with specified user_id does not exist.'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR) 

class ContactUs(APIView):
    permission_classes = [permissions.IsAuthenticated]
    def post(self, request, user_id):
        mobile_number = request.data.get('mobile_number')
        date = request.data.get('date')
        time = request.data.get('time')
        mode = request.data.get('mode')
        request.data['user'] = user_id
        serializer = ContactUsInfoSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        else:
            return Response(serializer.errors, status=400)
    
    def get(self, request, user_id):
        try:
            instance = ContactUsInfo.objects.all()
            serializer = ContactUsInfoSerializer(instance, many=True)
            return Response(serializer.data)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
    def put(self, request, user_id):
        try:
            instance = ContactUsInfo.objects.get(pk=user_id)
            serializer = ContactUsInfoSerializer(instance, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
    def delete(self, request, user_id):
        try:
            user = ContactUsInfo.objects.get(pk=user_id)
        except ContactUsInfo.DoesNotExist:
            return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
        user.delete()
        return Response({'message': 'User data deleted successfully'}, status=status.HTTP_204_NO_CONTENT)
    

class DeleteStaffuser(APIView):
    permission_classes = [permissions.IsAuthenticated]
    def post(self, request, user_id):
        try:
            staff_user = StaffUser.objects.get(id=user_id)
        except StaffUser.DoesNotExist:
            return Response({'error': 'Staff user does not exist'}, status=404)
        deleted_id = request.data.get('deleted_id')
        recently_visited = list(map(str, staff_user.recently_visited))
        #delete the data 
        final_recently_visited = []
        for visited_data in recently_visited:
            if visited_data != deleted_id:
                final_recently_visited.append(visited_data)
        staff_user.recently_visited = final_recently_visited
        staff_user.save()
        try:
            contract_instance = ContractsInfo.objects.get(candidate=deleted_id)
            contract_instance.delete()
        except ObjectDoesNotExist:
            pass  
        try:
            interview_instance = InterviewInfo.objects.get(candidate=deleted_id)
            interview_instance.delete()
        except ObjectDoesNotExist:
            pass  
        try:
            notification_instances = NotificationInfo.objects.filter(user=deleted_id)
            for notification_instance in notification_instances:
                notification_instance.delete()
        except (ObjectDoesNotExist, MultipleObjectsReturned):
            pass 
        return Response({
            'status': "User Data Deleted Successfully!!!",
            'recently_visited': final_recently_visited
        }, status=200)

class UpdateUserEmail(APIView):
    permission_classes = [permissions.IsAuthenticated]
    def post(self, request, user_id):
        email = request.data.get('email')
        username = request.data.get('username')
        try:
            staff_user = StaffUser.objects.get(pk=user_id)  
            serializer = StaffUserSerializer(staff_user, data=request.data) 
            if serializer.is_valid():
                staff_user.email = email  
                staff_user.username = username  
                staff_user.save()  
                return Response({"message": "Email and username updated successfully."})
            else:
                return Response({"error": serializer.errors}, status=400)
        except StaffUser.DoesNotExist:
            return Response({"error": "Staff user does not exist."}, status=404)
        except Exception as e:
            return Response({"error": str(e)}, status=500)
           
class Attachment(APIView):
    permission_classes = (permissions.AllowAny,)
    def post(self, request):
        job_title = request.data.get('job_title')
        resume_attachment = request.data.get('resume_attachment')
        to_email = "career@hirein5.com"
        if resume_attachment:
            email_body = 'Please find attached the resume for the job application for the position of: "' + job_title + '".'
            email = EmailMessage(
                subject='Resume for Job Application: {}'.format(job_title),
                body=email_body,
                from_email=settings.DEFAULT_FROM_EMAIL,
                to=[to_email]
            )
            email.attach(resume_attachment.name, resume_attachment.read(), 'application/pdf')
            email.send()
            return Response({'message': 'Email sent successfully.'}, status=status.HTTP_200_OK)
        else:
            return Response({'message': 'No resume attachment provided.'}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def WelcomeEmail(request):
    try:
        user_email = request.data.get('email')
        subject = request.data.get('subject')
        message = plain_message = request.data.get('message')
        subject = subject
        from_email = 'connect@hirein5.com'  
        to_email = user_email.lower()
        plain_message = message
        send_mail(subject, plain_message, from_email, [to_email])
        return Response({"success": "Email Sent Successfully!!!"}, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class PaymentInfo(APIView):
    permission_classes = (permissions.AllowAny,)
    def post(self,request):
            try:
                key_id = os.environ.get('key_id')
                key_secret = os.environ.get('key_secret')
                client = razorpay.Client(auth=(key_id, key_secret))
                amount = request.data.get('amount')
                # Create order
                order = client.order.create({
                    'amount': int(amount) * 100,
                    'currency': 'INR',
                    'payment_capture': 1 
                })
                return Response(order)
            except Exception as e:
                return Response({'error': str(e)}, status=500)
            
class PaymentInvoice(APIView):
    permission_classes = (permissions.AllowAny,)
    def post(self, request):
        try:
            key_id = os.environ.get('key_id')
            key_secret = os.environ.get('key_secret')
            client = razorpay.Client(auth=(key_id, key_secret))
            payment_id = request.data.get('payment_id')
            email = request.data.get('email')
            if not payment_id:
                raise ValueError("paymentId is missing in the request body")
            payment = client.payment.fetch(payment_id)
            amount = payment['amount']
            currency = payment['currency']
            customer = {
                'name': 'Customer Name',
                'email': 'customer@example.com',
                'contact': '1234567890',
            }
            invoice_data = {
                'type': 'invoice',
                'description': 'Invoice for payment',
                'customer': customer,
                'line_items': [
                    {
                        'name': 'Payment',
                        'description': 'Payment for goods/services',
                        'amount': amount,
                        'currency': currency,
                        'quantity': 1,
                    },
                ],
            }
            invoice = client.invoice.create(data=invoice_data)
            invoice_url = invoice["short_url"]
            subject = "Payment Receipt and Invoice"
            from_email = "connect@hirein5.com"
            to_email = [email]
            html_message = render_to_string('payment_invoice.html', {'invoice_url': invoice_url})
            email_message = EmailMessage(
                subject,
                html_message,
                from_email,
                to_email,
            )
            email_message.content_subtype = "html"
            email_message.send()
            return Response({"invoice_url": invoice_url, "success": "Invoice Email Sent Successfully"})
        except Exception as e:
            return Response({"error": str(e)}, status=500)