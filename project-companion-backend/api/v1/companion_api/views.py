from django.utils import timezone
from django.shortcuts import get_object_or_404
from django.urls import reverse
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view,permission_classes
from api.v1.pagination.pagination import StandardResultSetPagination
from .serializers import CompanionSerializer, DomainChoicesSerializer
from companion.models import Companion, DOMAIN_CHOICES
from api.v1.user_api.serializers import UserSerializer
from rest_framework.permissions import IsAuthenticated




# companion crud starts here
@api_view(["POST"])
@permission_classes([IsAuthenticated])
def create_companion(request):   
    serializer = CompanionSerializer(data=request.data)
    if serializer.is_valid():
        country = serializer.validated_data['country']
        state = serializer.validated_data['state']
        photo = serializer.validated_data.get("photo", "") or ""
        bio = serializer.validated_data.get('bio', "")
        phone = serializer.validated_data.get('phone', "")
        git_hub = serializer.validated_data.get('git_hub', "")
        linked_in = serializer.validated_data.get('linked_in', "")
        experience = serializer.validated_data.get('experience', "")
        domain = serializer.validated_data.get('domain', "")
        skills = serializer.validated_data.get('skills', "")
        qualification = serializer.validated_data.get('qualification', "")
        resume = serializer.validated_data.get('resume', "") or ""
        creator = request.user
        updator = request.user
        user = request.user

        if not Companion.objects.filter(user=user).exists():
            Companion(                    
                user = user, 
                country = country,
                state = state, 
                photo = photo, 
                bio = bio, 
                phone = phone, 
                git_hub = git_hub, 
                linked_in = linked_in, 
                experience = experience, 
                domain = domain, 
                skills = skills, 
                qualification = qualification,
                resume = resume,
                creator = creator,
                updator = updator
            ).save()
            response_data = {
                "status": 200,
                "title": "Successfully Created",
                "data":serializer.data,
                "message": "Companion created successfully.",
                "redirect": "true",
                "redirect_url": reverse('companion_api:companions')
            }
        else:               
            response_data = {
                "status": 400,
                "stable": "true",
                "error" : serializer.errors,
                "title": "Already exists",
                "message": "Companion already exists",                        
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
def companions(request):
    instances = Companion.objects.filter(is_deleted=False)
    paginator = StandardResultSetPagination()
    paginated_companions = paginator.paginate_queryset(instances, request)
    serializer = CompanionSerializer(paginated_companions, many=True)    
    response_data = {
        "status": 200,
        "message": "Companions List",
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


# @permission_classes([IsAuthenticated])
@api_view(["PATCH"])
def edit_companion(request):
    user = request.user
    instance = get_object_or_404(Companion.objects.filter(user=request.user, is_deleted=False))
    serializer = CompanionSerializer(instance=instance, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save(updator=user, date_updated=timezone.now())
        response_data = {
            "status":"true",
            "redirect":"true",
            "title":"Successfully Updated",
            "data":serializer.data,
            "message":"Companion Updated Successfully",
            "redirect_url":reverse('companion_api:companions')
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
def companion(request):
    instance = get_object_or_404(Companion.objects.filter(user=request.user,is_deleted=False))
    serializer = CompanionSerializer(instance)
    response_data = {
        "status_code" :200,
        "title" : "Companion Details",
        "data" : serializer.data
    }
    return Response(response_data)


@api_view(["PUT"])
def delete_companion(request,pk):
    instance = get_object_or_404(Companion, pk=pk)
    if not instance.is_deleted:
        instance.is_deleted = True
        instance.save()
    
    response_data = {
        "status" : 200,        
        "title" : "Successfully Deleted",
        "message" : "Companion Successfully Deleted.", 
        "redirect" : "true",       
        "redirect_url" : reverse('companion_api:companions')
    }
    return Response(response_data)

@api_view(['GET'])
def get_domain_choices(request):
    choices = [{'value': choice[0], 'display_name': choice[1]} for choice in DOMAIN_CHOICES]
    serializer = DomainChoicesSerializer(choices, many=True)
    response_data = {
        "status_code" :200,
        "title" : "Companion Details",
        "data" : serializer.data
    }
    return Response(response_data, status=status.HTTP_200_OK)

@api_view(['GET'])
def get_domain_choices(request):
    choices = [{'value': choice[0], 'display_name': choice[1]} for choice in DOMAIN_CHOICES]
    serializer = DomainChoicesSerializer(choices, many=True)
    response_data = {
        "status_code" :200,
        "title" : "Companion Details",
        "data" : serializer.data
    }
    return Response(response_data, status=status.HTTP_200_OK)