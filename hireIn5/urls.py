from django.urls import path, include
from rest_framework_simplejwt import views as jwt_views
from company.views import get_companies
from staff.views import *
from .views import symbolizeInitiated
from django.conf.urls.static import static
urlpatterns = [
    path('user/token/obtain/', ObtainTokenPairWithColorView.as_view(), name='token_create'),
    path('user/token/refresh/', jwt_views.TokenRefreshView.as_view(), name ='token_refresh'),
    path('user/logout/', LogoutView.as_view(), name='blacklist'),
    path('user/create/', StaffUserCreate.as_view(), name="create_user"),
    path('user/update/<int:user_id>/', UpdateStaffUser.as_view(), name='update_user'),
    path('user/emailverification/<int:user_id>', EmailVerification.as_view(), name='verify_email'),
    path('user/reset_password/', ForgotPassword.as_view(), name='reset_password'),
    path('user/update_password/', UpdatePassword.as_view(), name='update_password'),
    path('user/recentlyvisited/<int:user_id>', recently_visited, name='recently_visited'),
    path('remove/recentlyvisited/<int:user_id>', recently_visited, name='remove_recently_visited'),
    path('getFaculties/', get_faculties, name='get_faculties'),
    path('getCompanies/', get_companies, name='get_companies'),
    path('getUsersInformation/<int:user_id>/', getUserDetailInBulk, name='get_faculties'),
    path('', symbolizeInitiated, name="symbolizeInitiated"),
    path('bookmark/', include('bookmark.urls')),
    path('reservation/', include('reservation.urls')),
    path('cpadmin/', include('reservation.urls')),
    path('getTeamMembers/<int:user_id>/', get_team_members, name='get_team_members'),
    path('getContracts/<int:user_id>/', Contracts.as_view(), name='get_contracts'),
    path('getProffessionalDetails/<int:user_id>/', ProffessionalDetails.as_view(), name='getProffessionalDetails'),
    path('getProjectDetails/<int:user_id>/', ProjectDetails.as_view(), name='getProjectDetails'),
    path('getCertifications/<int:user_id>/', Certifications.as_view(), name='getCertifications'),
    path('getEducations/<int:user_id>/', Educations.as_view(), name='getEducations'),
    path('notification/<int:user_id>/', Notification.as_view(), name='notifications'),
    path('sendEmail/', EmailNotification.as_view(), name='emailnotifications'),
    path('role/staffusers/', get_by_roles, name='get_by_roles'),
    path('email/staffusers/', staff_data_by_email, name='getStaffusers'),
    path('getPricing/<int:user_id>/', PricingDetails.as_view(), name='pricing'),
    path('getInterview/<int:user_id>/', Interview.as_view(), name='interview'),
    path('update/password/', PasswordUpdate.as_view(), name='PasswordUpdate'),
    path('delete/staffuser/<int:user_id>/', DeleteStaffuser.as_view(), name='PasswordUpdate'),
    path('update/useremail/<int:user_id>/', UpdateUserEmail.as_view(), name='emailUpdate'),
    path('contactus/<int:user_id>/', ContactUs.as_view(), name='contactus'),
    path('payment/', PaymentInfo.as_view(), name='payment'),
    path('pdf/email/', Attachment.as_view(), name='pdf'),
    path('emails/', WelcomeEmail, name='WelcomeEmail'),
    path('payment/invoice/', PaymentInvoice.as_view(), name='PaymentInvoice'),

] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

