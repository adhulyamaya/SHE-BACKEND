from rest_framework import serializers
from rest_framework.serializers import ModelSerializer
from job.models import Job, JobApplication


class JobSerializer(ModelSerializer):
    class Meta:
        model = Job
        exclude = ['creator', 'updator', 'is_deleted']

class JobListSerializer(ModelSerializer):
    class Meta:
        model = Job
        exclude = ['creator', 'updator', 'is_deleted']

class JobApplicationSerializer(serializers.ModelSerializer):
    class Meta:
        model = JobApplication
        exclude = ['creator', 'updator', 'is_deleted']
