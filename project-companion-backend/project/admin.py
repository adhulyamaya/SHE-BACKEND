from django.contrib import admin
from .models import Project, ProjectComment, ProjectRequest

# Register your models here.
admin.site.register(Project)
admin.site.register(ProjectComment)
admin.site.register(ProjectRequest)