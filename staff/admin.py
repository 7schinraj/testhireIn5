from django.contrib import admin
from .models import *

class CustomUserAdmin(admin.ModelAdmin):
    model = StaffUser

admin.site.register(StaffUser, CustomUserAdmin)

admin.site.register(AddressInfo)
admin.site.register(KYCInfo)
admin.site.register(PassportInfo)
admin.site.register(Preference)
admin.site.register(TravelInfo)