from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework import serializers
from .models import *
from reservation.models import *
from company.serializers import CompanySerializer
from django.core.validators import EmailValidator
from company.models import CompanyInfo
class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super(MyTokenObtainPairSerializer, cls).get_token(user)
        token['first_name'] = user.first_name
        token['email'] = user.email
        token['phone'] = user.phone
        token['title'] = user.title
        token['linked_in'] = user.linked_in
        token['role'] = user.role
        token['onboarding_status'] = user.onboarding_status
        
        return token
       
    
class AddressInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = AddressInfo
        fields = '__all__'

class KYCInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = KYCInfo
        fields = '__all__'

class PassportInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = PassportInfo
        fields = '__all__'

class PreferenceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Preference
        fields = '__all__'

class TravelInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = TravelInfo
        fields = '__all__'

class PricingInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = PricingInfo
        fields = '__all__'
    
class ProfessionalDetailsInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProfessionalDetailsInfo
        fields = '__all__'

class WorkExperienceInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = WorkExperienceInfo
        fields = '__all__'

class ProjectDetailsInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProjectDetailsInfo
        fields = '__all__'

class CertificateInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = CertificateInfo
        fields = '__all__'

class EducationInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = EducationInfo
        fields = '__all__'

class ContractsInfoSerializer(serializers.ModelSerializer):
   
    class Meta:
        model = ContractsInfo
        fields = '__all__'

class TeamMembersInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = TeamMembersInfo
        fields = '__all__'

class RateCardInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = RateCardInfo
        fields = '__all__'

class NotificationInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = NotificationInfo
        fields = '__all__'

class InterviewInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = InterviewInfo
        fields = '__all__'

class ContactUsInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContactUsInfo
        fields = '__all__'

class HireInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = HireInfo
        fields = '__all__'

class ContactPreferenceSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContactPreferenceInfo
        fields = '__all__'

class RequirementsInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = RequirementsInfo
        fields = '__all__'

class StaffUserSerializer(serializers.ModelSerializer):
    address = AddressInfoSerializer(required=False)
    kyc_info = KYCInfoSerializer(required=False)
    passport_info = PassportInfoSerializer(required=False)
    preference_info = PreferenceSerializer(required=False)
    company = CompanySerializer(required=False)
    travel_info=TravelInfoSerializer(required=False)
    pricing_info = PricingInfoSerializer(required=False)
    professional_details_info = ProfessionalDetailsInfoSerializer(required=False)
    project_details_info = ProjectDetailsInfoSerializer(required=False)
    certificate_info = CertificateInfoSerializer(required=False)
    education_info = EducationInfoSerializer(required=False)
    work_preference_info=WorkExperienceInfoSerializer(required=False)
    contracts_info = ContractsInfoSerializer(required=False)
    team_members_info=TeamMembersInfoSerializer(required=False)
    rate_card_info=RateCardInfoSerializer(required=False)
    hire_info = HireInfoSerializer(required=False)
    contact_preference_info = ContactPreferenceSerializer(required=False)
    requirements_info = RequirementsInfoSerializer(required=False)
    
    class Meta:
        model = StaffUser
        fields = ('id', 'first_name', 'email', 'gender', 'username', 'password', 'phone','otp', 'title', 'linked_in', 'nottify',
                   'role', 'date_of_birth', 'current_place_of_residence','lived_at_current_residence','email_verification', 'mobile_verification',
                   'onboarding_status', 'profile_picture', 'part_time_availability', 'bio',"status", "apprual", 'employee_id', 'dissabled', 'hired_status','background_verification', 'personality_assessment',
                   'address','kyc_info', 'passport_info', 'preference_info','travel_info', 'company', 
                   'recently_visited',"pricing_info", "professional_details_info", 'project_details_info', 'certificate_info', 'hire_info',
                    'education_info', 'video_resume','work_preference_info','rate_card_info','contracts_info', 'team_members_info', 'interview_info', 'contact_preference_info', 'requirements_info')
        
        extra_kwargs = {'password': {'write_only': True, 'required': False},}

    def validate(self, data):
        if not data.get('username') and not data.get('email'):
            raise serializers.ValidationError({'username': 'Username or email is required.'})
        return data
    
    def create(self, validated_data):
        company_data = validated_data.pop('company', None)
        address_data = validated_data.pop('address', None)
        kyc_data = validated_data.pop('kyc_info', None)
        passport_data = validated_data.pop('passport_info', None)
        preference_data = validated_data.pop('preference_info', None)
        travelled_data = validated_data.pop('travel_info', None)
        pricing_data = validated_data.pop('pricing_info', None)
        work_preference_data = validated_data.pop('work_preference_info', None)
        rate_card_data = validated_data.pop('rate_card_info', None)
        hire_data = validated_data.pop('hire_info', None)
        contact_preference_data = validated_data.pop('contact_preference_info', None)
        requirements_info_data = validated_data.pop('requirements_info', None)

        if rate_card_data:
            rate_card_serializer=RateCardInfoSerializer(data=dict(rate_card_data))
            if rate_card_serializer.is_valid():
                rate_card_instance = rate_card_serializer.save()
                validated_data['rate_card_info'] = rate_card_instance
            else:
                raise serializers.ValidationError({'rate_card_info': rate_card_serializer.errors})

        if work_preference_data:
            work_preference_serializer=WorkExperienceInfoSerializer(data=dict(work_preference_data))
            if work_preference_serializer.is_valid():
                work_preference_instance = work_preference_serializer.save()
                validated_data['work_preference_info'] = work_preference_instance
            else:
                raise serializers.ValidationError({'work_preference_info': work_preference_serializer.errors})
            
        if company_data:
            company_serializer = CompanySerializer(data=dict(company_data))
            if company_serializer.is_valid():
                company_instance = company_serializer.save()
                validated_data['company'] = company_instance
            else:
                raise serializers.ValidationError({'company': company_serializer.errors})

        # Create and associate AddressInfo if provided
        if address_data:
            address_serializer = AddressInfoSerializer(data=dict(address_data))
            if address_serializer.is_valid():
                address_instance = address_serializer.save()
                validated_data['address'] = address_instance
            else:
                raise serializers.ValidationError({'address': address_serializer.errors})

        # Create and associate KYCInfo if provided
        if kyc_data:
            kyc_serializer = KYCInfoSerializer(data=dict(kyc_data))
            if kyc_serializer.is_valid():
                kyc_instance = kyc_serializer.save()
                validated_data['kyc_info'] = kyc_instance
            else:
                raise serializers.ValidationError({'kyc_info': kyc_serializer.errors})

        # Create and associate PassportInfo if provided
        if passport_data:
            passport_serializer = PassportInfoSerializer(data=dict(passport_data))
            if passport_serializer.is_valid():
                passport_instance = passport_serializer.save()
                validated_data['passport_info'] = passport_instance
            else:
                raise serializers.ValidationError({'passport_info': passport_serializer.errors})
            
        # Create and associate preference if provided
        if preference_data:
            preference_serializer = PreferenceSerializer(data=dict(preference_data))
            if preference_serializer.is_valid():
                preference_instance = preference_serializer.save()
                validated_data['preference_info'] = preference_instance
            else:
                raise serializers.ValidationError({'preference_info': preference_serializer.errors})
            
        # Create and associate travelinfo if provided
        if travelled_data:
            travelled_serializer =TravelInfoSerializer(data=dict(travelled_data))
            if travelled_serializer.is_valid():
                travelled_instance = travelled_serializer.save()
                validated_data['travel_info'] = travelled_instance
            else:
                raise serializers.ValidationError({'travel_info': travelled_serializer.errors})  
            
        if hire_data:
            hire_serializer = HireInfoSerializer(data=dict(hire_data))
            if hire_serializer.is_valid():
                hire_instance = hire_serializer.save()
                validated_data['hire_info'] = hire_instance
            else:
                raise serializers.ValidationError({'hire_info': hire_serializer.errors})
             
        if contact_preference_data:
            contact_preference_serializer = ContactPreferenceSerializer(data=dict(contact_preference_data))
            if contact_preference_serializer.is_valid():
                contact_preference_instance = contact_preference_serializer.save()
                validated_data['contact_preference_info'] = contact_preference_instance
            else:
                raise serializers.ValidationError({'contact_preference_info': contact_preference_serializer.errors}) 
            
        if requirements_info_data:
            requirements_serializer = RequirementsInfoSerializer(data=dict(requirements_info_data))
            if requirements_serializer.is_valid():
                requirements_instance = requirements_serializer.save()
                validated_data['requirements_info'] = requirements_instance
            else:
                raise serializers.ValidationError({'requirements_info': requirements_serializer.errors})

        # Handle password field
        password = validated_data.pop('password', None)
        instance = self.Meta.model(**validated_data)

        if password is not None:
            instance.set_password(password)
            
        instance.save()
        return instance

    def update(self, instance, validated_data):
        # Update user fields
        instance.first_name = validated_data.get('first_name', instance.first_name)
        instance.email = validated_data.get('email', instance.email)
        instance.username = validated_data.get('username', instance.username)
        instance.phone = validated_data.get('phone', instance.phone)
        instance.title = validated_data.get('title', instance.title)
        instance.linked_in = validated_data.get('linked_in', instance.linked_in)
        instance.role = validated_data.get('role', instance.role)
        instance.email_verification=validated_data.get('email_verification', instance.email_verification)
        instance.mobile_verification=validated_data.get('mobile_verification', instance.mobile_verification)
        instance.current_place_of_residence=validated_data.get('current_place_of_residence', instance.current_place_of_residence)
        instance.lived_at_current_residence=validated_data.get('lived_at_current_residence', instance.lived_at_current_residence)
        instance.video_resume=validated_data.get('video_resume', instance.video_resume)
        instance.date_of_birth=validated_data.get('date_of_birth', instance.date_of_birth)
        instance.part_time_availability=validated_data.get('part_time_availability', instance.part_time_availability)
        instance.bio=validated_data.get('bio', instance.bio)
        instance.gender=validated_data.get('gender', instance.gender)
        instance.onboarding_status=validated_data.get('onboarding_status', instance.onboarding_status)
        instance.profile_picture=validated_data.get('profile_picture', instance.profile_picture)
        instance.status=validated_data.get('status', instance.status)
        instance.apprual=validated_data.get('apprual', instance.apprual)
        instance.employee_id=validated_data.get('employee_id', instance.employee_id)
        instance.dissabled=validated_data.get('dissabled', instance.dissabled)
        instance.hired_status=validated_data.get('hired_status', instance.hired_status)
        instance.nottify=validated_data.get('nottify', instance.nottify)
        instance.interview_status=validated_data.get('interview_status', instance.interview_status)
        instance.background_verification=validated_data.get('background_verification', instance.background_verification)
        instance.personality_assessment=validated_data.get('personality_assessment', instance.personality_assessment)
        instance.fresher=validated_data.get('fresher', instance.fresher)
        instance.mr=validated_data.get('mr', instance.mr)
        instance.mrs=validated_data.get('mrs', instance.mrs)


        hire_data = validated_data.get('hire_info', None)
        if hire_data:
            hire_serializer = HireInfoSerializer(instance.hire_info, data=hire_data)
            if hire_serializer.is_valid():
                hire_instance = hire_serializer.save()
                instance.hire_info = hire_instance
            else:
                raise serializers.ValidationError({'hire_info': hire_serializer.errors})
        elif 'hire_info' in validated_data:
            # If 'hire_info' is provided with null value, remove the existing association
            instance.hire_info = None

        requirements_info_data = validated_data.get('requirements_info', None)
        if requirements_info_data:
            requirements_info_serializer = RequirementsInfoSerializer(instance.requirements_info, data=requirements_info_data)
            if requirements_info_serializer.is_valid():
                requirements_info_instance = requirements_info_serializer.save()
                instance.requirements_info = requirements_info_instance
            else:
                raise serializers.ValidationError({'requirements_info': requirements_info_serializer.errors})
        elif 'requirements_info' in validated_data:
            # If 'requirements_info' is provided with null value, remove the existing association
            instance.requirements_info = None

        contact_preference_data = validated_data.get('contact_preference_info', None)
        if contact_preference_data:
            contact_preference_serializer = ContactPreferenceSerializer(instance.contact_preference_info, data=contact_preference_data)
            if contact_preference_serializer.is_valid():
                contact_preference_instance = contact_preference_serializer.save()
                instance.contact_preference_info = contact_preference_instance
            else:
                raise serializers.ValidationError({'contact_preference_info': contact_preference_serializer.errors})
        elif 'contact_preference_info' in validated_data:
            # If 'contact_preference_info' is provided with null value, remove the existing association
            instance.contact_preference_info = None

        work_preference_data=validated_data.get('work_preference_info', None)
        if work_preference_data:
            work_preference_serializer = WorkExperienceInfoSerializer(instance.work_preference_info, data=work_preference_data)
            if work_preference_serializer.is_valid():
                work_preference_instance = work_preference_serializer.save()
                instance.work_preference_info = work_preference_instance
            else:
                raise serializers.ValidationError({'work_preference_info': work_preference_serializer.errors})
        elif 'work_preference_info' in validated_data:
            # If 'work_preference_info' is provided with null value, remove the existing association
            instance.work_preference_info = None

        company_data = validated_data.get('company', None)
        if company_data:
            company_serializer = CompanySerializer(instance.company, data=company_data)
            if company_serializer.is_valid():
                company_instance = company_serializer.save()
                instance.company = company_instance
            else:
                raise serializers.ValidationError({'company': company_serializer.errors})
        elif 'company' in validated_data:
            # If 'company' is provided with null value, remove the existing association
            instance.company = None

        # Update or create the associated address
        address_data = validated_data.get('address', None)
        if address_data:
            address_serializer = AddressInfoSerializer(instance.address, data=address_data)
            if address_serializer.is_valid():
                address_instance = address_serializer.save()
                instance.address = address_instance
            else:
                raise serializers.ValidationError({'address': address_serializer.errors})
        elif 'address' in validated_data:
            # If 'address' is provided with null value, remove the existing association
            instance.address = None

        # Update or create the associated KYC info
        kyc_data = validated_data.get('kyc_info', None)
        if kyc_data:
            kyc_serializer = KYCInfoSerializer(instance.kyc_info, data=kyc_data)
            if kyc_serializer.is_valid():
                kyc_instance = kyc_serializer.save()
                instance.kyc_info = kyc_instance
            else:
                raise serializers.ValidationError({'kyc_info': kyc_serializer.errors})
        elif 'kyc_info' in validated_data:
            # If 'kyc_info' is provided with null value, remove the existing association
            instance.kyc_info = None

        # Update or create the associated passport info
        passport_data = validated_data.get('passport_info', None)
        if passport_data:
            passport_serializer = PassportInfoSerializer(instance.passport_info, data=passport_data)
            if passport_serializer.is_valid():
                passport_instance = passport_serializer.save()
                instance.passport_info = passport_instance
            else:
                raise serializers.ValidationError({'passport_info': passport_serializer.errors})
        elif 'passport_info' in validated_data:
            # If 'passport_info' is provided with null value, remove the existing association
            instance.passport_info = None

        # Update or create the associated prefferance
        preference_data = validated_data.get('preference_info', None)
        if preference_data:
            preference_serializer=PreferenceSerializer(instance.preference_info, data=preference_data)
            if preference_serializer.is_valid():
                preferance_instance= preference_serializer.save()
                instance.preference_info= preferance_instance
            else:
                raise serializers.ValidationError({'preference_info': preference_serializer.errors})
            
        elif 'preference_info' in validated_data:
            instance.preference_info= None
        # Update or create the associated travel information
        travelled_data = validated_data.get('travel_info', None)
        if travelled_data:
            travelled_serializer = TravelInfoSerializer(instance.travel_info, data=travelled_data)
            if travelled_serializer.is_valid():
                travelled_instance = travelled_serializer.save()
                instance.travel_info = travelled_instance
            else:
                raise serializers.ValidationError({'travel_info': travelled_serializer.errors})
        elif 'travel_info' in validated_data:
            instance.travel_info = None
        
        rate_card_data = validated_data.get('rate_card_info', None)
        if rate_card_data:
            rate_card_serializer = RateCardInfoSerializer(instance.rate_card_info, data=rate_card_data)
            if rate_card_serializer.is_valid():
                rate_card_instance = rate_card_serializer.save()
                instance.rate_card_info = rate_card_instance
            else:
                raise serializers.ValidationError({'rate_card_info': rate_card_serializer.errors})
        elif 'rate_card_info' in validated_data:
            # If 'address' is provided with null value, remove the existing association
            instance.rate_card_info = None

        instance.save()
        return instance