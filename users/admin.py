from django.contrib import admin
from .models import CustomUser,EmailCode
admin.site.register([CustomUser,EmailCode])