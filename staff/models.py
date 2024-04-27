from django.contrib.auth.models import AbstractUser
from django.contrib.auth import get_user_model
from django.db import models
from company.models import CompanyInfo
from datetime import date
from django.contrib.postgres.fields import ArrayField
from django.utils import timezone

class AddressInfo(models.Model):    
    address = models.CharField(max_length=255, blank=True, default='')
    city = models.CharField(max_length=30, blank=True, default='')
    state = models.CharField(max_length=30, blank=True, default='')
    pincode = models.IntegerField(default=0)
    country = models.CharField(max_length=50,blank=True, default='')

class KYCInfo(models.Model):
    aadhar_number = models.CharField(max_length=15, default='')
    aadhar_front = models.CharField(max_length=255, blank=True, default='')
    aadhar_back = models.CharField(max_length=255, blank=True, default='')
    pan_number = models.CharField(max_length=15, blank=True, default='')
    pan_front = models.CharField(max_length=255, blank=True, default='')
    
class PassportInfo(models.Model):
    passport_number = models.CharField(max_length=15, blank=True, default='')
    passport_validity = models.CharField(max_length=100, blank=True, default="")
    country_of_citizenship = models.CharField(max_length=100, blank=True, default='')
    country_of_issue = models.CharField(max_length=100, blank=True, default='')
    passport_front = models.CharField(max_length=255, blank=True, default='')
    passport_back = models.CharField(max_length=255, blank=True, default='')

class Preference(models.Model):
    qualification = models.CharField(null=True, max_length=100, default='')
    year_of_experience = models.IntegerField(default=0)
    skills = ArrayField(models.CharField(max_length=200), blank=True, default=list)
    linkedin = models.CharField(max_length=255, default='')
    hackerrank = models.CharField(max_length=255, blank=True, default='')
    github = models.CharField(max_length=255, blank=True, default='')
    personal_website = models.CharField(max_length=255, blank=True, default='')
    language = ArrayField(models.CharField(max_length=200), blank=True, default=list)
    
class TravelInfo(models.Model):
    travelled_to= ArrayField(models.CharField(max_length=200), blank=True, default=list)
    travel_to_for_work = ArrayField(models.CharField(max_length=200, blank=True, default=list))
    relocate_for_work =  models.CharField(max_length=255, blank=True, default='')
    willingness =  models.CharField(max_length=255, blank=True, default='')
    duration = models.CharField(max_length=50, blank=True, default='')
    prefered_countries = ArrayField(models.CharField(max_length=200), blank=True, null=True, default=list)

class PricingInfo(models.Model):
    user = models.CharField(blank=True, max_length=64, default='')
    pricing_plan=models.CharField(blank=True, max_length=64, default='')
    plan_validity=models.CharField(blank=True, max_length=64, default='')
    plan_price=models.CharField(blank=True, max_length=64, default='')
    plan_duration=models.CharField(blank=True, max_length=64, default='')
    plan_start=models.DateTimeField(auto_now_add=True)
    plan_status=models.CharField(blank=True, max_length=64, default='')
    invoice_url = models.CharField(blank=True, max_length=255, default='')

# candidate profile details fields
class ProfessionalDetailsInfo(models.Model):
    user=models.CharField(max_length=10, blank=True, default="")
    title=models.CharField(max_length=100, blank=True, default='')
    years_active=models.CharField(max_length=100, blank=True, default='')
    company_name=models.CharField(max_length=100, blank=True, default='')
    skills = ArrayField(models.CharField(max_length=200), blank=True, default=list)
    location= models.CharField(max_length=100, blank=True, default='')
    description=models.TextField(blank=True, default='')
    annual_salary=models.CharField(max_length=100, blank=True, default='')
    currency = models.CharField(max_length=100, blank=True, default='')

class ProjectDetailsInfo(models.Model):
    user=models.CharField(max_length=10, blank=True, default="")
    project_title=models.CharField(max_length=50, blank=True, default='')
    role=models.CharField(max_length=50, blank=True, default='')
    reporting_to=models.CharField(max_length=50, blank=True, default='')
    duration_of_project=models.CharField(max_length=50, blank=True, default='')
    skills = ArrayField(models.CharField(max_length=200), blank=True, default=list)
    description=models.TextField(blank=True, default='')

class CertificateInfo(models.Model):
    user=models.CharField(max_length=10, blank=True, default="")
    course_name=models.CharField(max_length=50, blank=True, default='')
    date_issued=models.CharField(max_length=50, blank=True, default='')
    skills = ArrayField(models.CharField(max_length=200), blank=True, default=list)
    url=models.CharField(max_length=255, blank=True, default='')
    description=models.TextField(max_length=255, blank=True, default='')
    certificate_file=ArrayField(models.CharField(max_length=200), blank=True, default=list)
    validity_date= models.CharField(max_length=10, blank=True, default="")

class EducationInfo(models.Model):
    user=models.CharField(max_length=10, blank=True, default="")
    degree=models.CharField(max_length=50, blank=True, default='')
    year_of_graduation=models.CharField(max_length=10, blank=True, default='')
    university_name=models.CharField(max_length=50, blank=True, default='')
    education_level=models.CharField(max_length=50, blank=True, default='')
    cgpa=models.CharField(max_length=50, blank=True, default='')
    study_mode=models.CharField(max_length=50, blank=True, default='')
    upload_file=ArrayField(models.CharField(max_length=200), blank=True, default=list)

class WorkExperienceInfo(models.Model):
    key_skills=ArrayField(models.CharField(max_length=200), blank=True, default=list)
    current_employment_status=models.CharField(max_length=50, blank=True, default='')
    preferred_mode_of_engagement=models.CharField(max_length=50, blank=True, default='')
    preferred_method_of_work=ArrayField(models.CharField(max_length=200), blank=True, default=list)
    preffered_work_location= ArrayField(models.CharField(max_length=200), blank=True, default=list)
    preffered_work_timings= models.CharField(max_length=50, blank=True, default='')
    language= ArrayField(models.CharField(max_length=200), blank=True, default=list)
    website_url=models.CharField(max_length=255, blank=True, default='')
    hackerrank_url=models.CharField(max_length=255, blank=True, default='')
    github_url=models.CharField(max_length=255, blank=True, default='')
#newly added tables
class ContractsInfo(models.Model):
    user=models.CharField(max_length=10, blank=True, default="")
    file=models.CharField(max_length=255, blank=True, default="")
    uplaod_date=models.DateTimeField(auto_now=True)
    name=models.CharField(max_length=255, blank=True, default="")
    date=models.CharField(max_length=20, blank=True, default="")
    duration=models.CharField(max_length=20, blank=True, default="")
    billing_cycle= models.CharField(max_length=100, blank=True, default="")
    candidate = models.CharField(max_length=10, blank=True, default="")

class TeamMembersInfo(models.Model):
    name=models.CharField(max_length=50, blank=True, default="")
    email_id=models.CharField(max_length=255, blank=True, default="")
    level_of_access=models.CharField(max_length=255, blank=True)
    status=models.CharField(max_length=255, blank=True, default="")

class RateCardInfo(models.Model):
    remote_hourly=models.CharField(max_length=50, blank=True, default="")
    remote_monthly=models.CharField(max_length=50, blank=True, default="")
    remote_annualy=models.CharField(max_length=50, blank=True, default="")
    onsite_hourly=models.CharField(max_length=50, blank=True, default="")
    onsite_monthly=models.CharField(max_length=50, blank=True, default="")
    onsite_annualy=models.CharField(max_length=50, blank=True, default="")

class NotificationInfo(models.Model):
    user = models.CharField(max_length=100, blank=True, default="")
    message = models.CharField(max_length=255, blank=True, default="")
    created_at = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=100, blank=True, default="")
    on_type = models.CharField(max_length=100, blank=True, default="")

class InterviewInfo(models.Model):
    user = models.CharField(max_length=10, blank=True, default="")
    date = models.CharField(max_length=100, blank=True, default="")
    candidate = models.CharField(max_length=10, blank=True, default="")
    time = models.CharField(max_length=10, blank=True, default="")
    meeting_url = models.CharField(max_length=255, blank=True, default="")

class ContactUsInfo(models.Model):
    mobile_number = models.CharField(max_length=50, blank=True, default="")
    date = models.CharField(max_length=50, blank=True, default="")
    time = models.CharField(max_length=50, blank=True, default="")
    user = models.CharField(max_length=50, blank=True, default="")
    mode = models.CharField(max_length=50, blank=True, default="")

class HireInfo(models.Model):
    candidate_id = models.CharField(blank=True, max_length=100, default='')
    company_name = models.CharField(blank=True, max_length=100, default='')
    client_id = models.CharField(blank=True, max_length=100, default='')
    contract_id = models.CharField(blank=True, max_length=100, default='')

class ContactPreferenceInfo(models.Model):
    prefered_mode = ArrayField(models.CharField(max_length=200), blank=True, default=list)
    date = models.CharField(max_length=50, blank=True, default="")
    time = models.CharField(max_length=50, blank=True, default="")
    time_zone = models.CharField(max_length=50, blank=True, default="")

class RequirementsInfo(models.Model):
    looking_for = ArrayField(models.CharField(max_length=200), blank=True, default=list)
    duration = models.CharField(max_length=20, blank=True, default='')
    skills = ArrayField(models.CharField(max_length=200), blank=True, default=list)
    budget = models.CharField(max_length=20, blank=True, default='')
    currency = models.CharField(max_length=20, blank=True, default='')
    location = models.CharField(max_length=20, blank=True, default='')

class StaffUser(AbstractUser):
    phone = models.CharField(blank=True, max_length=15, default='')
    title = models.CharField(blank=True, max_length=50, default='')
    linked_in = models.CharField(blank=True, max_length=255, default='')
    role = models.CharField(blank=True, max_length=10, default='')
    date_of_birth = models.CharField(blank=True, max_length=10, default='')
    email_verification = models.BooleanField(default=False)
    mobile_verification = models.BooleanField(default=False)
    current_place_of_residence = models.CharField(max_length=200, blank=True, default="")
    date_of_birth=models.CharField(max_length=20, blank=True, default="")
    video_resume=models.CharField(max_length=255, default='',blank=True)
    # gender=models.CharField(max_length=10, default='',blank=True)
    profile_picture=models.CharField(max_length=255, default='',blank=True)
    lived_at_current_residence = models.CharField(max_length=200, blank=True, default="")
    company = models.ForeignKey(CompanyInfo, on_delete=models.CASCADE, null=True, blank=True, related_name='staff_users')
    address = models.ForeignKey(AddressInfo, on_delete=models.CASCADE, null=True,  blank=True)
    kyc_info = models.ForeignKey(KYCInfo, on_delete=models.CASCADE, null=True,  blank=True)
    passport_info = models.ForeignKey(PassportInfo, on_delete=models.CASCADE, null=True, blank=True)
    preference_info = models.ForeignKey(Preference, on_delete=models.CASCADE, blank=True, null=True)
    travel_info = models.ForeignKey(TravelInfo, on_delete=models.CASCADE, null=True, blank=True)
    # forget_info = models.ForeignKey(ForgotInfo, on_delete=models.CASCADE, null=True, blank=True)
    recently_visited = ArrayField(models.IntegerField(null=True, blank=True), blank=True, default=list)
    pricing_info = models.ForeignKey(PricingInfo, on_delete=models.CASCADE, null=True,  blank=True)
    onboarding_status = models.CharField(max_length=2, blank=True, default=1)
    professional_details_info = models.ForeignKey(ProfessionalDetailsInfo, on_delete=models.CASCADE, null=True, blank=True)
    hire_info = models.ForeignKey(HireInfo, on_delete=models.CASCADE, null=True, blank=True)
    project_details_info = models.ForeignKey(ProjectDetailsInfo, on_delete=models.CASCADE, null=True, blank=True)
    certificate_info = models.ForeignKey(CertificateInfo, on_delete=models.CASCADE, null=True, blank=True)
    education_info = models.ForeignKey(EducationInfo, on_delete=models.CASCADE, null=True, blank=True)
    work_preference_info = models.ForeignKey(WorkExperienceInfo, on_delete=models.CASCADE, null=True, blank=True)
    rate_card_info = models.ForeignKey(RateCardInfo, on_delete=models.CASCADE, null=True, blank=True)
    status=models.CharField(max_length=255, blank=True, default="")
    apprual=models.BooleanField(default=False)
    employee_id=models.CharField(max_length=255, blank=True, default="")
    dissabled=models.BooleanField(default=False)
    hired_status=models.CharField(max_length=255, blank=True, default="")
    contracts_info=models.ForeignKey(ContractsInfo, on_delete=models.CASCADE, null=True, blank=True)
    team_members_info=models.ForeignKey(TeamMembersInfo, on_delete=models.CASCADE, null=True, blank=True)
    bio=models.CharField(max_length=500, blank=True, default="")
    part_time_availability=models.CharField(max_length=100, blank=True, default="")
    nottify = models.BooleanField(default=False)
    background_verification = models.CharField(max_length=255, blank=True, default="")
    personality_assessment = models.CharField(max_length=255, blank=True, default="")
    interview_info = models.ForeignKey(InterviewInfo, on_delete=models.CASCADE, null=True, blank=True)
    otp = models.CharField(max_length=6, blank=True, null=True, default="")
    interview_status = models.CharField(max_length=6, blank=True, null=True, default=False)
    fresher = models.CharField(max_length=6, blank=True, null=True, default=False)
    mr = models.CharField(max_length=5, blank=True, null=True, default="")
    mrs = models.CharField(max_length=5, blank=True, null=True, default="")
    contact_preference_info = models.ForeignKey(ContactPreferenceInfo, on_delete=models.CASCADE, null=True, blank=True)
    requirements_info = models.ForeignKey(RequirementsInfo, on_delete=models.CASCADE, null=True, blank=True)
    test_field_status = models.CharField(max_length=5, blank=True, null=True, default="")