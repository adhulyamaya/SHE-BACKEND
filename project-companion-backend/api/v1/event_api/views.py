from django.utils import timezone
from django.shortcuts import get_object_or_404
from django.urls import reverse
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view,permission_classes
from api.v1.pagination.pagination import StandardResultSetPagination
from .serializers import EventSerializer,EventRegistrationSerializer
from event.models import Event,  EventRegistration
from api.v1.user_api.serializers import UserSerializer
from rest_framework.permissions import IsAuthenticated




# event crud starts here
@api_view(["POST"])
@permission_classes([IsAuthenticated])
def create_event(request):   
    serializer = EventSerializer(data=request.data)
    if serializer.is_valid():
        title = serializer.validated_data['title']
        description = serializer.validated_data['description']
        organizer = request.user
        event_date = serializer.validated_data['event_date']
        event_time = serializer.validated_data['event_time']
        duration = serializer.validated_data['duration']
        venue = serializer.validated_data['venue']
        is_online = serializer.validated_data['is_online']
        url = serializer.validated_data['url']
        poster = serializer.validated_data['poster']
        creator = request.user
        updator = request.user
        
        if event_date <= timezone.now().date():  # Changed: Added validation for future date
            return Response({
                "status": 400,
                "stable": "true",
                "title": "Invalid Date",
                "message": "Event date must be in the future.",
            })

        if not Event.objects.filter(title=title).exists():
            Event(                    
                title = title, 
                description = description,
                organizer = organizer, 
                event_date = event_date, 
                event_time = event_time, 
                duration = duration, 
                venue = venue, 
                is_online = is_online, 
                url = url, 
                poster=poster,
                creator = creator,
                updator = updator
            ).save()
            response_data = {
                "status": 200,
                "title": "Successfully Created",
                "data":serializer.data,
                "message": "Event created successfully.",
                "redirect": "true",
                "redirect_url": reverse('event_api:events')
            }
        else:               
            response_data = {
                "status": 400,
                "stable": "true",
                "error" : serializer.errors,
                "title": "Already exists",
                "message": "Event already exists",                        
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
def allEvents(request):
    today = timezone.now().date()
    instances = Event.objects.filter(is_deleted=False, event_date__gte=today)
    paginator = StandardResultSetPagination()
    paginated_events = paginator.paginate_queryset(instances, request)
    serializer = EventSerializer(paginated_events, many=True)    
    response_data = {
        "status": 200,
        "message": "events List",
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
@permission_classes([IsAuthenticated])
def myEvents(request):
    instances = Event.objects.filter(creator=request.user,is_deleted=False)
    paginator = StandardResultSetPagination()
    paginated_events = paginator.paginate_queryset(instances, request)
    serializer = EventSerializer(paginated_events, many=True)    
    response_data = {
        "status": 200,
        "message": "events List",
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
def edit_event(request, pk):
    instance = get_object_or_404(Event.objects.filter(pk=pk, is_deleted=False))
    serializer = EventSerializer(instance=instance, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save(updator=request.user, date_updated=timezone.now())
        response_data = {
            "status":"true",
            "redirect":"true",
            "title":"Successfully Updated",
            "data":serializer.data,
            "message":"Event Updated Successfully",
            "redirect_url":reverse('event_api:events')
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
def event(request, pk):
    instance = get_object_or_404(Event.objects.filter(pk=pk,is_deleted=False))
    serializer = EventSerializer(instance)
    response_data = {
        "status_code" :200,
        "title" : "Event Details",
        "data" : serializer.data
    }
    return Response(response_data)


@api_view(["PUT"])
def delete_event(request,pk):
    instance = get_object_or_404(Event, pk=pk)  
    if not instance.is_deleted:
        instance.is_deleted = True
        instance.save() 
        
    response_data = {
        "status" : 200,        
        "title" : "Successfully Deleted",
        "message" : "Event Successfully Deleted.", 
        "redirect" : "true",       
        "redirect_url" : reverse('event_api:events')
    }
    return Response(response_data)


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def create_event_registration(request):   
    serializer = EventRegistrationSerializer(data=request.data)
    print('serializer',serializer)
    if serializer.is_valid():
        event = serializer.validated_data.get('event') 
        user = request.user

        if not EventRegistration.objects.filter(event=event, user=user).exists():
            EventRegistration.objects.create(
                event=event,
                user=user,
                creator = user,
                updator = user
            )
            response_data = {
                "status": 200,
                "title": "Successfully Registered",
                "data": serializer.data,
                "message": "Event registration created successfully.",
                "redirect": "true",
                "redirect_url": reverse('event_api:event-registration')
            }
        else:
            response_data = {
                "status": 400,
                "stable": "true",
                "error": serializer.errors,
                "title": "Already Registered",
                "message": "You have already registered for this event.",
            }
    else:
        response_data = {
            "stable": "true",
            "status": 400,
            "error": serializer.errors,
            "title": "Form Validation Error",
            "message": "Validation error.",
        }
    return Response(response_data)

@api_view(["GET"])
def event_registrations(request):
    instances = EventRegistration.objects.filter(user=request.user)
    paginator = StandardResultSetPagination()
    paginated_registrations = paginator.paginate_queryset(instances, request)
    serializer = EventRegistrationSerializer(paginated_registrations, many=True)
    response_data = {
        "status": 200,
        "message": "Event Registrations List",
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
def event_registration(request, pk):
    instance = get_object_or_404(EventRegistration, pk=pk, user=request.user)
    serializer = EventRegistrationSerializer(instance)
    response_data = {
        "status": 200,
        "title": "Event Registration Details",
        "data": serializer.data,
    }
    return Response(response_data)

@api_view(["PUT"])
def cancel_event_registration(request, pk):
    instance = get_object_or_404(EventRegistration, pk=pk)
    if not instance.is_cancel:
        instance.is_cancel = True
        instance.save() 
    response_data = {
        "status": 200,
        "title": "Successfully Deleted",
        "message": "Event Registration Successfully Deleted.",
        "redirect": "true",
        "redirect_url": reverse('event_api:event-registration')
    }
    return Response(response_data)
