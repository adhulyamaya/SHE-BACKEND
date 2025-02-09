from django.urls import reverse
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from api.v1.pagination.pagination import StandardResultSetPagination
from api.v1.job_api.serializers import JobListSerializer, JobSerializer, JobApplicationSerializer
from rest_framework.response import Response
from django.utils import timezone
from job.models import Job, JobApplication
from django.utils import timezone
from main.management.commands.create_groups_and_permissions import IsHr, IsCompanion




# job crud starts here
@api_view(["POST"])
# @permission_classes([IsAuthenticated])
def create_job(request):   
    serializer = JobSerializer(data=request.data)
    if serializer.is_valid():
        title = serializer.validated_data['title']
        description = serializer.validated_data['description']
        salary_from = serializer.validated_data['salary_from']
        salary_to = serializer.validated_data['salary_to']
        experience = serializer.validated_data['experience']
        skills = serializer.validated_data['skills']
        company = serializer.validated_data['company']
        creator = request.user
        updator = request.user

        if not Job.objects.filter(title=title,company=company).exists():
            Job(                    
                title = title, 
                description = description,
                salary_from = salary_from, 
                salary_to = salary_to, 
                experience = experience, 
                skills = skills, 
                company = company,
                creator = creator,
                updator = updator
            ).save()
            response_data = {
                "status": 200,
                "title": "Successfully Created",
                "message": "Job created successfully.",
                "data":serializer.data,
                "redirect": "true",
                "redirect_url": reverse('job_api:jobs')
            }
        else:
            print("error1",serializer.errors)               
            response_data = {
                "status": 400,
                "stable": "true",
                "error":serializer.errors,
                "title": "Already exists",
                "message": "Job already exists",                        
            }
    else:  
        print("error2",serializer.errors)      
        response_data = {
            "stable": "true",
            "status": 400,
            "error":serializer.errors,
            "title": "Form validation error",
            "message": "Validation Error",               
        }
    return Response(response_data)


@api_view(["GET"])
def jobs(request):
    instances = Job.objects.filter(is_deleted=False)
    paginator = StandardResultSetPagination()
    paginated_jobs = paginator.paginate_queryset(instances, request)
    serializer = JobSerializer(paginated_jobs, many=True)    
    response_data = {
        "status": 200,
        "message": "Jobs List",
        "data": serializer.data,
        "meta": {
            "count": paginator.page.paginator.count,
            "pagination": {
                "next": paginator.get_next_link(),
                "previous": paginator.get_previous_link(),
            }
        }
    }    
    return Response(response_data)


@api_view(["PATCH"])
@permission_classes([IsAuthenticated, IsHr])
def edit_job(request, pk):
    instance = get_object_or_404(Job.objects.filter(pk=pk, is_deleted=False))
    serializer = JobSerializer(instance=instance, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save(updator=request.user, date_updated=timezone.now())
        response_data = {
            "status":"true",
            "redirect":"true",
            "title":"Successfully Updated",
            "data":serializer.data,
            "message":"Job Updated Successfully",
            "redirect_url":reverse('job_api:jobs')
        }
    else:
        response_data = {
            "stable":"true",
            "status":"false",
            "error" : serializer.errors,
            "message":"Validation Error",
            "title":"Form validation errr"
        }
    return Response(response_data)


@api_view(["GET"])
def job(request, pk):
    instance = get_object_or_404(Job.objects.filter(pk=pk, is_deleted=False))
    serializer = JobSerializer(instance)
    response_data = {
        "status_code": 200,
        "title": "Job Details",
        "data": serializer.data
    }
    return Response(response_data)


@api_view(["PUT"])
@permission_classes([IsAuthenticated, IsHr])
def delete_job(request,pk):
    instance = get_object_or_404(Job.objects.filter(pk=pk,is_deleted=False))  
    Job.objects.filter(pk=pk).update(is_deleted=True,title=instance.title + "_deleted_" )    
    response_data = {
        "status" : 200,        
        "title" : "Successfully Deleted",
        "message" : "Job Successfully Deleted.", 
        "redirect" : "true",       
        "redirect_url" : reverse('job_api:jobs')
    }
    return Response(response_data)


@api_view(['POST'])
@permission_classes([IsAuthenticated, IsCompanion])
def apply_job(request):
    print(request.data, request.user)

    data = request.data.copy()  # Copy the request data
    data['applicant'] = request.user.id  # Set the applicant field to the current user ID
    
    serializer = JobApplicationSerializer(data=data)
    
    if serializer.is_valid():
        serializer.save(creator=request.user, updator=request.user)  # Save with creator and updator

        response_data = {
            "status": 200,
            "title": "Application Submitted",
            "message": "Your job application has been submitted successfully.",
            "data": serializer.data,
            "redirect": True,
            # "redirect_url": reverse('job_api:jobs')  # Assuming 'applications' is the name of your job applications list endpoint
        }
        return Response(response_data, status=status.HTTP_201_CREATED)
    else:
        response_data = {
            "status": 400,
            "stable": True,
            "error": serializer.errors,
            "title": "Validation Error",
            "message": "Form validation error"
        }
        return Response(response_data, status=status.HTTP_400_BAD_REQUEST)
    
@api_view(['PUT'])
@permission_classes([IsAuthenticated, IsHr])
def manage_application_status(request, pk):
    try:
        application = JobApplication.objects.get(pk=pk)
    except JobApplication.DoesNotExist:
        return Response({
            "status": 404,
            "title": "Not Found",
            "message": "Job application not found."
        }, status=status.HTTP_404_NOT_FOUND)
    
    # Only update the status field
    if 'status' not in request.data:
        return Response({
            "status": 400,
            "title": "Validation Error",
            "message": "Status field is required."
        }, status=status.HTTP_400_BAD_REQUEST)
    
    application.status = request.data['status']
    
    # Validate the new status value using the serializer
    serializer = JobApplicationSerializer(application, data=request.data, partial=True)
    if serializer.is_valid():
        response_data = {
            "status": 200,
            "title": "Application Status Updated",
            "message": "Application status has been updated successfully.",
            "data": serializer.data
        }
        return Response(response_data)
    
    return Response({
        "status": 400,
        "title": "Validation Error",
        "message": "Form validation error",
        "errors": serializer.errors
    }, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([IsAuthenticated, IsHr])
def list_applications_for_job(request, job_id):
    applications = JobApplication.objects.filter(job_id=job_id)
    serializer = JobApplicationSerializer(applications, many=True)
    response_data = {
        "status": 200,
        "title": "Job Applications List",
        "message": "List of applications for the specified job.",
        "data": serializer.data
    }
    return Response(response_data)

@api_view(['GET'])
@permission_classes([IsAuthenticated, IsCompanion])
def list_applications_by_companion(request, companion_id):
    applications = JobApplication.objects.filter(applicant_id=companion_id)
    serializer = JobApplicationSerializer(applications, many=True)
    response_data = {
        "status": 200,
        "title": "Applications by Companion",
        "message": "List of applications submitted by the specified companion.",
        "data": serializer.data
    }
    return Response(response_data)