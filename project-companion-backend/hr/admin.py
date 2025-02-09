from django.contrib import admin
from .models import Hr, JobPost, JobPostApplication

# Register your models here.
admin.site.register(Hr)
admin.site.register(JobPost)
admin.site.register(JobPostApplication)