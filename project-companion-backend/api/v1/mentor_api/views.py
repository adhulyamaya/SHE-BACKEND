from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from mentor.models import Mentor, MentorshipRequest
from companion.models import Companion
from project.models import Project
from .serializers import MentorSerializer, MentorshipRequestSerializer
from api.v1.pagination.pagination import SetPagination,StandardResultSetPagination
from rest_framework.decorators import api_view
from django.urls import reverse
from django.utils import timezone
from django.db.models import Q



# mentor crud starts here
@api_view(["POST"])
@permission_classes([IsAuthenticated])
def create_mentor(request):
    serializer = MentorSerializer(data=request.data)
    if serializer.is_valid():        
        country = serializer.validated_data['country']
        state = serializer.validated_data['state']
        photo = serializer.validated_data.get('photo')
        bio = serializer.validated_data.get('bio')
        phone = serializer.validated_data['phone']
        git_hub = serializer.validated_data.get('git_hub')
        linked_in = serializer.validated_data.get('linked_in')
        experience = serializer.validated_data.get('experience')
        domain = serializer.validated_data.get('domain')
        payment_method = serializer.validated_data['payment_method']
        creator = request.user
        updator = request.user
        user = request.user

        if not Mentor.objects.filter(user=user).exists():
            Mentor.objects.create(
                user=user,
                country=country,
                state=state,
                photo=photo,
                bio=bio,
                phone=phone,
                git_hub=git_hub,
                linked_in=linked_in,
                experience=experience,
                domain=domain,
                payment_method=payment_method,
                creator = creator,
                updator = updator
            )
            response_data = {
                "status": 200,
                "title": "Successfully Created",
                "message": "Mentor created successfully.",
                "data":serializer.data,
                "redirect": "true",
                "redirect_url": reverse('mentor_api:mentors')
            }
        else:
            response_data = {
                "status": 400,
                "stable": "true",
                "error":serializer.errors,
                "title": "Already exists",
                "message": "Mentor already exists",
            }
    else:
        response_data = {
            "stable": "true",
            "status": 400,
            "error":serializer.errors,
            "title": "Form validation error",
            "message": "Validation Error",
        }
    return Response(response_data)


@api_view(["GET"])
def mentors(request):
    instances = Mentor.objects.filter(is_deleted=False)

    keyword_query = request.GET.get("keywords")
    if keyword_query:
        instances = instances.filter(Q(domain__icontains=keyword_query) | Q(user__first_name__icontains=keyword_query) | Q(user__last_name__icontains=keyword_query) | Q(experience__icontains=keyword_query))    
    paginator = StandardResultSetPagination()
    paginated_mentors = paginator.paginate_queryset(instances, request)
    serializer = MentorSerializer(paginated_mentors, many=True)    
    response_data = {
        "status": 200,
        "message": "Mentors List",
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
def edit_mentor(request):
    try:
        # Retrieve Mentor instance or 404 if not found
        instance = get_object_or_404(Mentor.objects.filter(user=request.user, is_deleted=False))
        
        # Initialize serializer with instance and request data
        serializer = MentorSerializer(instance=instance, data=request.data, partial=True)
        
        # Validate serializer data
        if serializer.is_valid():
            # Save validated data to instance
            serializer.save(updator=request.user, date_updated=timezone.now())
            print('Mentor updated successfully:', serializer.data)
            
            # Respond with success message and updated data
            return Response({
                "status": "success",
                "message": "Mentor updated successfully",
                "data": serializer.data,
                "redirect_url": reverse('mentor_api:mentors')  # Adjust as needed
            })
        else:
            # Handle validation errors
            return Response({
                "status": "error",
                "message": "Validation Error",
                "errors": serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)
    
    except Mentor.DoesNotExist:
        # Handle case where Mentor instance is not found
        return Response({
            "status": "error",
            "message": "Mentor not found or deleted"
        }, status=status.HTTP_404_NOT_FOUND)
    
    except Exception as e:
        # Handle unexpected exceptions
        return Response({
            "status": "error",
            "message": str(e)
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



@api_view(["GET"])
def mentor(request):
    instance = get_object_or_404(Mentor.objects.filter(user=request.user, is_deleted=False))
    serializer = MentorSerializer(instance)
    response_data = {
        "status_code": 200,
        "title": "Mentor Details",
        "data": serializer.data
    }
    return Response(response_data)


@api_view(["PUT"])
def delete_mentor(request, pk):
    instance = get_object_or_404(Mentor.objects.filter(pk=pk, is_deleted=False))
    Mentor.objects.filter(pk=pk).update(is_deleted=True) 
    response_data = {
        "status": 200,
        "title": "Successfully Deleted",
        "message": "Mentor Successfully Deleted.",
        "redirect": "true",
        "redirect_url": reverse('mentor_api:mentors')  
    }
    return Response(response_data)

@api_view(["POST"])
def send_mentorship_request(request):
    print(request.data)
    
    # Retrieve the Companion instance associated with the authenticated user
    companion = get_object_or_404(Companion, user=request.user)

    # Check if the user has the 'companion' role
    if not request.user.roles.filter(name='companion').exists():
        response_data = {
            "status": 400,
            "title": "Role Error",
            "message": "You must have the Companion role to send mentorship requests."
        }
        return Response(response_data, status=400)

    # Add the companion instance to the request data for validation
    request_data = request.data.copy()
    request_data['companion'] = companion.id

    # Validate request data
    serializer = MentorshipRequestSerializer(data=request_data)
    if not serializer.is_valid():
        print('Serializer errors:', serializer.errors)  # Debugging
        return Response(serializer.errors, status=400)

    # Create mentorship request instance
    mentorship_request = MentorshipRequest(
        companion=companion,
        mentor_id=request_data.get('mentor'),
        project_id=request_data.get('project'),
        status='pending',
        creator_id=request.user.id,  # Set the creator_id to the authenticated user's ID
        updator_id=request.user.id   # Set the updator_id to the authenticated user's ID
    )
    mentorship_request.save()

    response_data = {
        "status": 200,
        "title": "Request Sent",
        "message": "Mentorship request sent successfully.",
        "data": MentorshipRequestSerializer(mentorship_request).data,
    }
    return Response(response_data)

@api_view(["GET"])
def check_request_exists(request):
    mentor_id = request.GET.get('mentor')
    project_id = request.GET.get('project')

    print(f"Received mentor_id: {mentor_id}, project_id: {project_id}")
    
    if not mentor_id or not project_id:
        return Response({'exists': False}, status=400)

    # Check for an existing request
    exists = MentorshipRequest.objects.filter(
        companion__user=request.user,
        mentor_id=mentor_id,
        project_id=project_id,
        status='pending'
    ).exists()

    return Response({'exists': exists})

@api_view(["GET"])
def get_mentorship_requests(request):

    # Retrieve the Mentor instance associated with the authenticated user
    mentor = get_object_or_404(Mentor, user=request.user)

    # Fetch all mentorship requests for this mentor
    mentorship_requests = MentorshipRequest.objects.filter(mentor=mentor, status='pending')

    # Serialize the mentorship requests
    serializer = MentorshipRequestSerializer(mentorship_requests, many=True)

    # Return the serialized data
    return Response({
        "status": 200,
        "title": "Mentorship Requests",
        "data": serializer.data,
    })

@api_view(["POST"])
def handle_mentorship_request(request, pk):

    # Retrieve the MentorshipRequest instance
    mentorship_request = get_object_or_404(MentorshipRequest, id=pk)

    # Determine action from request data
    action = request.data.get('action')
    
    if action == 'accept':
        # Update the status of the request to "accepted"
        mentorship_request.status = 'accepted'
    elif action == 'reject':
        # Update the status of the request to "rejected"
        mentorship_request.status = 'rejected'
    else:
        return Response({"detail": "Invalid action."}, status=400)

    # Save the updated request
    mentorship_request.save()

    # Response data
    response_data = {
        "status": 200,
        "title": f"Request {action.capitalize()}ed",
        "message": f"The mentorship request has been {action}ed successfully.",
        "data": {
            "id": mentorship_request.id,
            "companion": mentorship_request.companion.user.email,
            "mentor": mentorship_request.mentor.user.email,
            "project": mentorship_request.project.name,
            "status": mentorship_request.status,
        },
    }

    return Response(response_data, status=status.HTTP_200_OK)