from django.db import models
from django.contrib.postgres.fields import ArrayField



class CompanyInfo(models.Model):
    company_email = models.CharField(max_length=200, null=True, blank=True)
    company_name = models.CharField(max_length=60, null=True, blank=True)
    company_location = models.CharField(max_length=255, null=True, blank=True)
    company_url = models.CharField(max_length=255, null=True, blank=True)
    company_register_no=models.CharField(max_length=20, null=True, blank=True)
    verified = models.BooleanField(default=False)
    terms = models.BooleanField(default=False)
    plan_selected = models.IntegerField(default=0)
    plan_expiry = models.DateField(null=True)
    interested_in = ArrayField(models.CharField(max_length=100), blank=True, null=True)
    looking_for = ArrayField(models.CharField(max_length=100), blank=True, null=True)
    duration = ArrayField(models.CharField(max_length=100), blank=True, null=True)
    agree_terms = models.BooleanField(default=False)
    notes = models.CharField(max_length=200, null=True, blank=True)
    billing_company = models.CharField(max_length=60, null=True, blank=True)
    billing_address = models.CharField(max_length=255, null=True, blank=True)
    company_pan = models.CharField(max_length=20, null=True, blank=True)
    primary_name = models.CharField(max_length=50, null=True, blank=True)
    primary_email = models.CharField(max_length=50, null=True, blank=True)
    primary_phone = models.CharField(max_length=50, null=True, blank=True)
    secondary_name = models.CharField(max_length=50, null=True, blank=True)
    secondary_email = models.CharField(max_length=50, null=True, blank=True)
    secondary_phone = models.CharField(max_length=50, null=True, blank=True)
    pincode = models.CharField(max_length=30, null=True, blank=True)
    country = models.CharField(max_length=30, null=True, blank=True)