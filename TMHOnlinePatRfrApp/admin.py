from django.contrib import admin
from .models import referral_details,profile,role_master

# Register your models here.

admin.site.register(referral_details)

admin.site.register(profile)

admin.site.register(role_master)