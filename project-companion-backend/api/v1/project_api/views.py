from django.conf import settings
from django.utils import timezone
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from api.v1.pagination.pagination import StandardResultSetPagination
from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from django.urls import reverse
from api.v1.project_api.serializers import ProjectListSerializer, ProjectSerializer, ProjectCommentSerializer, ProjectCommentListSerializer, ProjectRequestSerializer, ProjectRequestListSerializer
from project.models import ProjectComment, Project, ProjectRequest
from companion.models import Companion
from project_companion_backend.settings import FRONTEND_URL
from user.tasks import send_bulk_comment_notification



# Project CRUD starts here
@api_view(["POST"])
def create_project(request):   
    serializer = ProjectSerializer(data=request.data)
    if serializer.is_valid():
        project = serializer.save(leader=request.user, creator=request.user, updator=request.user)
        # Ensure the project leader has the 'project_team_member' role
        # request.user.roles.get_or_create(name='project_team_member')
        response_data = {
            "status": 200,
            "title": "Successfully Created",
            "data": ProjectSerializer(project).data,
            "message": "Project created successfully.",
            "redirect": "true",
            "redirect_url": reverse('project_api:projects')
        }
    else:        
        response_data = {
            "stable": "true",
            "status": 400,
            "error": serializer.errors,
            "title": "Form validation error",
            "message": "Validation Error",               
        }
    return Response(response_data)

@api_view(["GET"])
def projects(request):
    instances = Project.objects.filter(is_active=True)
    
    keyword_query = request.GET.get("keywords")
    if keyword_query:
        instances = instances.filter(Q(name__icontains=keyword_query) | Q(description__icontains=keyword_query))    

    paginator = StandardResultSetPagination()
    paginated_projects = paginator.paginate_queryset(instances, request)
    serializer = ProjectListSerializer(paginated_projects, many=True, context={'user': request.user})    
    response_data = {
        "status": 200,
        "message": "Projects List",
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

@api_view(["GET"])
def my_projects(request):
    companion = Companion.objects.filter(user=request.user).first()
    print(companion)
    if not companion:
        return Response({
            "status": status.HTTP_404_NOT_FOUND,
            "message": "Companion profile not found."
        }, status=status.HTTP_404_NOT_FOUND)
        
    instances = Project.objects.filter(is_active=True, leader=companion)   
    paginator = StandardResultSetPagination()
    paginated_projects = paginator.paginate_queryset(instances, request)
    serializer = ProjectListSerializer(paginated_projects, many=True, context={'user': request.user}) 
    response_data = {
        "status": 200,
        "message": "Projects List",
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
def edit_project(request, pk):
    print("called")
    instance = get_object_or_404(Project.objects.filter(pk=pk, is_active=True))
    serializer = ProjectSerializer(instance=instance, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save(updator=request.user, date_updated=timezone.now())        
        response_data = {
            "status": "true",
            "redirect": "true",
            "title": "Successfully Updated",
            "message": "Project updated successfully.",                
            "redirect_url": reverse('project_api:projects')
        }
    else:
        response_data = {
            "stable": "true",
            "status": "false",
            "error": serializer.errors,
            "message": "Validation Error",
            "title": "Form validation error"  
        }
    return Response(response_data)

@api_view(["GET"])
def project(request, pk):
    instance = get_object_or_404(Project.objects.filter(pk=pk, is_active=True))
    serializer = ProjectSerializer(instance=instance)
    response_data = {
        "status_code": 200,
        "title": "Project Details",
        "data": serializer.data
    }
    return Response(response_data)

@api_view(["PUT"])
def delete_project(request, pk):
    instance = get_object_or_404(Project.objects.filter(pk=pk, is_deleted=False))  
    Project.objects.filter(pk=pk).update(is_active=False, is_deleted=True)    
    response_data = {
        "status": 200,        
        "title": "Successfully Deleted",
        "message": "Project Successfully Deleted.", 
        "redirect": "true",       
        "redirect_url": reverse('project_api:projects')  
    }
    return Response(response_data)


@api_view(["POST"])
def create_project_comment(request):
    print(request.data)
    serializer = ProjectCommentSerializer(data=request.data)
    if serializer.is_valid():
        user = request.user
        try:
            companion = Companion.objects.get(user=user)
        except Companion.DoesNotExist:
            companion = None

        project = serializer.validated_data['project']
        comment = serializer.validated_data['comment']
        image = serializer.validated_data.get('image', None)
        file = serializer.validated_data.get('file', None)
        
        project_comment = ProjectComment.objects.create(
            project=project,
            companion=companion,
            comment=comment,
            image=image,
            file=file,
            creator=user,
            updator=user
        )
        
        # Fetch all team member emails from the project team
        team_members = project.team.all()
        recipients = [member.user.email for member in team_members if member.user.email]

        # Prepare email subject, project URL, and other details for the notification
        subject = f"New Comment on Project: {project.name}"
        project_url = f"{FRONTEND_URL}/projects/{project.id}"  # Replace with your actual frontend URL
        companion_username = companion.user.username if companion else "Unknown User"

        # Send email notifications to the team members
        send_bulk_comment_notification.delay(
            recipients=recipients,
            subject=subject,
            companion_username=companion_username,
            project=project,
            comment=comment,
            project_url=project_url,
            comment_added_by=user
        )

        response_data = {
            "status": 200,
            "title": "Successfully Created",
            "data": ProjectCommentSerializer(project_comment).data,
            "message": "Project Comment created successfully.",
            "redirect": "true",
            "redirect_url": reverse('project_api:projects')
        }
    else:
        print("comment serializer not valid ", serializer.errors)
        response_data = {
            "stable": "true",
            "status": 400,
            "error": serializer.errors,
            "title": "Form validation error",
            "message": "Validation Error",
        }
    return Response(response_data)

@api_view(["GET"])
def project_comments(request,pk):
    instances = ProjectComment.objects.filter(project_id=pk,is_deleted=False)
    paginator = StandardResultSetPagination()
    paginated_comments = paginator.paginate_queryset(instances, request)
    serializer = ProjectCommentListSerializer(paginated_comments, many=True)

    response_data = {
        "status": 200,
        "message": "Project Comments List",
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

@api_view(["GET"])
def project_comment(request, pk):
    """
    Retrieve a specific project comment by its primary key (project_id).
    """
    instance = get_object_or_404(ProjectComment.objects.filter(project_id=pk, is_deleted=False))
    serializer = ProjectCommentSerializer(instance)
    response_data = {
        "status": 200,
        "title": "Project Comment Details",
        "data": serializer.data
    }
    return Response(response_data)

@api_view(["PUT"])
def edit_project_comment(request, pk):
    instance = get_object_or_404(ProjectComment, pk=pk, is_deleted=False)
    serializer = ProjectCommentSerializer(instance=instance, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save(updator=request.user, date_updated=timezone.now())
        response_data = {
            "status": "true",
            "redirect": "true",
            "title": "Successfully Updated",
            "message": "Project comment updated successfully.",
            "redirect_url": reverse('project_api:projects')
        }
    else:
        response_data = {
            "stable": "true",
            "status": "false",
            "error": serializer.errors,
            "message": "Validation Error",
            "title": "Form validation error"
        }
    return Response(response_data)

@api_view(["PUT"])
def delete_project_comment(request, pk):
    instance = get_object_or_404(ProjectComment, pk=pk, is_deleted=False)
    instance.is_deleted = True
    instance.save()

    response_data = {
        "status": 200,
        "title": "Successfully Deleted",
        "message": "Project Comment Successfully Deleted.",
        "redirect": "true",
        "redirect_url": reverse('project_api:projects')
    }
    return Response(response_data)

@api_view(["POST"])
def send_project_request(request):
    # Retrieve the Companion instance associated with the authenticated user
    companion = get_object_or_404(Companion, user=request.user)
    
    # Check if the user has the 'companion' role
    if not request.user.roles.filter(name='companion').exists():
        response_data = {
            "status": 400,
            "title": "Role Error",
            "message": "You must have the Companion role to send project requests."
        }
        return Response(response_data, status=400)
    
    # Validate request data
    serializer = ProjectRequestSerializer(data=request.data)
    if not serializer.is_valid():
        return Response(serializer.errors, status=400)
    
    # Create project request instance
    project_request = ProjectRequest(
        project_id=request.data.get('project'),
        sender=companion,
        receiver_id=request.data.get('receiver'),
        status='pending',
        creator_id=request.user.id,  # Set the creator_id to the authenticated user's ID
        updator_id=request.user.id   # Set the updator_id to the authenticated user's ID
    )
    project_request.save()

    response_data = {
        "status": 200,
        "title": "Request Sent",
        "message": "Project request sent successfully.",
        "data": ProjectRequestSerializer(project_request).data,
    }
    return Response(response_data)

@api_view(["PUT"])
def respond_to_project_request(request, pk):
    # Retrieve the project request object or return 404 if not found
    project_request = get_object_or_404(ProjectRequest, pk=pk)
    
    # Check if the user is authenticated
    if not request.user.is_authenticated:
        response_data = {
            "status": 403,
            "title": "Unauthorized",
            "message": "User is not authenticated.",
        }
        return Response(response_data)
    
    print(f"Request user: {request.user}")
    print(f"Project request receiver: {project_request.receiver}")

    # Check if the user is the receiver of the request
    if request.user.email != project_request.receiver.user.email:
        response_data = {
            "status": 403,
            "title": "Unauthorized",
            "message": "You are not authorized to respond to this request.",
        }
        return Response(response_data)
    
    # Check if 'response' field is present in request data
    if 'response' not in request.data:
        response_data = {
            "status": 400,
            "title": "Response Missing",
            "message": "Response field is required.",
        }
        return Response(response_data)
    
    response = request.data['response']
    
    # Update the project request status based on the response
    if response == 'accept':
        project_request.status = 'accepted'
        # Add the receiver to the project team and assign the 'project_team_member' role
        if project_request.receiver not in project_request.project.team.all():
            project_request.project.team.add(project_request.receiver)
            # project_request.receiver.user.roles.get_or_create(name='project_team_member')
        
    elif response == 'reject':
        project_request.status = 'rejected'
    else:
        response_data = {
            "status": 400,
            "title": "Invalid Response",
            "message": "Invalid response value. Use 'accept' or 'reject'.",
        }
        return Response(response_data)

    # Save the updated project request
    project_request.save()

    # Serialize the project request object
    serializer = ProjectRequestSerializer(project_request)
    
    # Construct response data
    response_data = {
        "status": 200,
        "title": "Request Responded",
        "message": f"Request {response}ed successfully.",
        "data": serializer.data,
    }

    return Response(response_data)


@api_view(["GET"])
def list_project_requests(request):
    project_requests = ProjectRequest.objects.all()
    serializer = ProjectRequestListSerializer(project_requests, many=True)
    response_data = {
        "status": 200,
        "message": "List of all project requests.",
        "data": serializer.data,
    }
    return Response(response_data)


@api_view(["GET"])
def list_project_requests_for_receiver(request, receiver_id):
    # Assuming receiver_id is the ID of the user who is the receiver
    project_requests = ProjectRequest.objects.filter(receiver_id=receiver_id)
    serializer = ProjectRequestListSerializer(project_requests, many=True)
    response_data = {
        "status": 200,
        "message": f"List of project requests for receiver {receiver_id}.",
        "data": serializer.data,
    }
    return Response(response_data)