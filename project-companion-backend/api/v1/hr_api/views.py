from django.utils import timezone
from django.shortcuts import get_object_or_404
from django.urls import reverse
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from api.v1.pagination.pagination import StandardResultSetPagination
from .serializers import HrSerializer, HrJobPostSerializer, JobApplicationSerializer
from hr.models import Hr, JobPost, JobPostApplication
from companion.models import Companion
from api.v1.user_api.serializers import UserSerializer
from django.db.models import Q




# hr crud starts here
@api_view(["POST"])
def create_hr(request):   
    serializer = HrSerializer(data=request.data)
    if serializer.is_valid():
        company_name = serializer.validated_data['company_name']
        state = serializer.validated_data['state']
        photo = serializer.validated_data['photo']
        phone = serializer.validated_data['phone']
        linked_in = serializer.validated_data['linked_in']
        country = serializer.validated_data['country']
        creator = request.user
        updator = request.user
        user = request.user

        if not Hr.objects.filter(user=user).exists():
            Hr(                    
                user = user, 
                company_name=company_name,
                country = country,
                state = state, 
                photo = photo, 
                phone = phone, 
                linked_in = linked_in, 
                creator = creator,
                updator = updator                
            ).save()
            response_data = {
                "status": 200,
                "title": "Successfully Created",
                "data":serializer.data,
                "message": "Hr created successfully.",
                "redirect": "true",
                # "redirect_url": reverse('hr_api:hrs')
            }
        else:               
            response_data = {
                "status": 400,
                "stable": "true",
                "error" : serializer.errors,
                "title": "Already exists",
                "message": "hr already exists",                        
            }
    else:        
        response_data = {
            "stable": "true",
            "status": 400,
            "error" : serializer.errors,
            "title": "Form validation error",
            "message": "Validation Error",               
        }
    return Response(response_data)


@api_view(["GET"])
def hrs(request):
    instances = Hr.objects.filter(is_deleted=False)
    paginator = StandardResultSetPagination()
    paginated_hrs = paginator.paginate_queryset(instances, request)
    serializer = HrSerializer(paginated_hrs, many=True)    
    response_data = {
        "status": 200,
        "message": "Hr List",
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


@api_view(["PUT"])
def edit_hr(request):
    instance = get_object_or_404(Hr.objects.filter(user=request.user, is_deleted=False))
    serializer = HrSerializer(instance=instance, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save(updator=request.user, date_updated=timezone.now())
        response_data = {
            "status":"true",
            "redirect":"true",
            "title":"Successfully Updated",
            "message":"Hr Updated Successfully",
            "redirect_url":reverse('hr_api:hrs')
        }
    else:
        response_data = {
            "stable":"true",
            "status":"false",
            "error":serializer.errors,
            "message":"Validation Error",
            "title":"Form validation error"
        }
    return Response(response_data)


@api_view(["GET"])
def hr(request):
    instance = get_object_or_404(Hr.objects.filter(user=request.user,is_deleted=False))
    serializer = HrSerializer(instance=instance)
    response_data = {
        "status_code" :200,
        "title" : "Hr Details",
        "data" : serializer.data
    }
    return Response(response_data)


@api_view(["PUT"])
def delete_hr(request,pk):
    instance = get_object_or_404(Hr.objects.filter(pk=pk,is_deleted=False))  
    Hr.objects.filter(pk=pk).update(is_deleted=True)    
    response_data = {
        "status" : 200,        
        "title" : "Successfully Deleted",
        "message" : "Hr Successfully Deleted.", 
        "redirect" : "true",       
        "redirect_url" : reverse('hr_api:hrs')
    }
    return Response(response_data)


# job_post crud starts here

@api_view(["POST"])
def create_job_post(request):   
    print('calling job_post')
    serializer = HrJobPostSerializer(data=request.data)
    if serializer.is_valid():
        print('valid serializer')
        user = request.user
        
        # Ensure the user is linked to an Hr instance
        try:
            hr = Hr.objects.filter(user=user).first()
        except Hr.DoesNotExist:
            return Response(
                {"error": "User is not an HR."},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        title = serializer.validated_data['title']
        description = serializer.validated_data['description']
        salary_from = serializer.validated_data['salary_from']
        salary_to = serializer.validated_data['salary_to']
        experience = serializer.validated_data['experience']
        skills = serializer.validated_data['skills']
        company = serializer.validated_data['company']
        location = serializer.validated_data['location']
        hr = hr
        creator = request.user
        updator = request.user

        if not JobPost.objects.filter(hr=hr, title=title, is_deleted=False).exists():
            job_post = JobPost(                    
                hr=hr, 
                title=title,
                description=description,
                salary_from=salary_from, 
                salary_to=salary_to, 
                experience=experience, 
                skills=skills, 
                company=company,
                location=location,
                creator=creator,
                updator=updator
            )
            job_post.save()
            print('job created')
            response_data = {
                "status": 200,
                "title": "Successfully Created",
                "data": serializer.data,
                "message": "hrJobPost created successfully.",
                "redirect": "true",
                # "redirect_url": reverse('hr_api:hrs')
            }
        else:   
            print('job already exists')            
            response_data = {
                "status": 400,
                "stable": "true",
                "error": serializer.errors,
                "title": "Already exists",
                "message": "hrJobPost already exists",                        
            }
    else:      
        print('invalid data')  
        print(serializer.errors)  # Print the serializer errors for debugging
        response_data = {
            "stable": "true",
            "status": 400,
            "error": serializer.errors,
            "title": "Form validation error",
            "message": "Validation Error",               
        }
    return Response(response_data)



@api_view(["GET"])
def job_posts(request):
    hr = Hr.objects.filter(user=request.user).first()
    instances = JobPost.objects.filter(hr=hr,is_deleted=False)

    keyword_query = request.GET.get("keywords")
    if keyword_query:
        instances = instances.filter(Q(title__icontains=keyword_query) | Q(description__icontains=keyword_query) | Q(experience__icontains=keyword_query) | Q(skills__icontains=keyword_query))    

    paginator = StandardResultSetPagination()
    paginated_hrs = paginator.paginate_queryset(instances, request)
    serializer = HrJobPostSerializer(paginated_hrs, many=True)    
    print(serializer.data)
    response_data = {
        "status": 200,
        "message": "hrJobPosts List",
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
def edit_job_post(request, pk):
    instance = get_object_or_404(JobPost.objects.filter(pk=pk, is_deleted=False))
    serializer = HrJobPostSerializer(instance=instance, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save(updator=request.user, date_updated=timezone.now())
        response_data = {
            "status": "true",
            "redirect": "true",
            "title": "Successfully Updated",
            "message": "hrJobPosts Updated Successfully",
            # "redirect_url": reverse('hr_api:hrs')
        }
    else:
        response_data = {
            "status": "false",
            "error": serializer.errors,
            "message": "Validation Error",
            "title": "Form validation error"
        }
    return Response(response_data)

@api_view(["GET"])
def all_job_posts(request):
    # Fetch all job posts
    instances = JobPost.objects.filter(is_deleted=False)
    
    keyword_query = request.GET.get("keywords")
    if keyword_query:
        instances = instances.filter(Q(title__icontains=keyword_query) | Q(description__icontains=keyword_query) | Q(experience__icontains=keyword_query) | Q(skills__icontains=keyword_query))    

    serializer = HrJobPostSerializer(instance=instances, many=True)
    
    response_data = {
        "status_code": 200,
        "title": "All Job Posts",
        "data": serializer.data
    }
    
    return Response(response_data)



@api_view(["GET"])
def job_post(request, pk):
    instance = get_object_or_404(JobPost.objects.filter(pk=pk,is_deleted=False))
    serializer = HrJobPostSerializer(instance=instance)
    print(serializer.data)
    response_data = {
        "status_code" :200,
        "title" : "hrJobPosts Details",
        "data" : serializer.data
    }
    return Response(response_data)


@api_view(["PUT"])
def delete_job_post(request,pk):
    instance = get_object_or_404(JobPost.objects.filter(pk=pk,is_deleted=False))  
    JobPost.objects.filter(pk=pk).update(is_deleted=True)    
    response_data = {
        "status" : 200,        
        "title" : "Successfully Deleted",
        "message" : "hrJobPost Successfully Deleted.", 
        "redirect" : "true",       
        "redirect_url" : reverse('hr_api:hrs')
    }
    return Response(response_data)

# @api_view(['PUT'])
# def toggle_block_job(request, pk):
#     try:
#         job = get_object_or_404(JobPost, id=pk)
#         job.is_blocked = not job.is_blocked
#         job.save()
#         status = 'unblocked' if job.is_blocked else 'blocked'
#         return Response({'success': True, 'message': f'Job has been {status} successfully.'})
#     except Exception as e:
#         print(e)
#         return Response({'success': False, 'message': str(e)}, status=400)


@api_view(['POST'])
def apply_for_job(request):
    job_id = request.data.get('job_id')
    job = get_object_or_404(JobPost, pk=job_id)
    applicant = Companion.objects.filter(user=request.user, is_deleted=False).first()
    existing_application = JobPostApplication.objects.filter(job=job, companion=applicant).first()

    if existing_application:
        return Response({'error': 'You have already applied for this job'}, status=status.HTTP_400_BAD_REQUEST)

    application = JobPostApplication(
        job=job, 
        companion=applicant, 
        status='applied', 
        creator=request.user,  # Set the creator field
        updator = request.user
    )
    application.save()

    return Response({'message': 'Application submitted successfully'}, status=status.HTTP_201_CREATED)

@api_view(['GET'])
def job_applicants_list(request, pk):
    try:
        job = JobPost.objects.get(id=pk)
        applications = JobPostApplication.objects.filter(job=job)
        serializer = JobApplicationSerializer(applications, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except JobPost.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    

@api_view(['GET'])
def user_job_applications_list(request):
    try:
        companion = Companion.objects.filter(user=request.user).first()
        applications = JobPostApplication.objects.filter(companion=companion)
        serializer = JobApplicationSerializer(applications, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except JobPostApplication.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)