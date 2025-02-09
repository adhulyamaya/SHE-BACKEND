from django.utils import timezone
from django.shortcuts import get_object_or_404
from django.urls import reverse
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view,permission_classes
from api.v1.pagination.pagination import StandardResultSetPagination
from api.v1.contributor_api.serializers import ContributorSerializer,ContributorCreateSerializer, StatusChoicesSerializer, TaskSerializer, ContributorTaskSerializer, UnitChoicesSerializer
from contributor.models import CONTRIBUTOR_TASK_CHOICES, UNIT_CHOICES, Contributor, ContributorTask, Task
from api.v1.user_api.serializers import UserSerializer
from rest_framework.permissions import IsAuthenticated
from user.models import CustomUser, Role



@api_view(['GET'])
def get_status_choices(request):
    choices = [{'value': choice[0], 'display_name': choice[1]} for choice in CONTRIBUTOR_TASK_CHOICES]
    serializer = StatusChoicesSerializer(choices, many=True)
    response_data = {
        "status_code" :200,
        "title" : "Companion Details",
        "data" : serializer.data
    }
    return Response(response_data, status=status.HTTP_200_OK)

@api_view(['GET'])
def get_unit_choices(request):
    choices = [{'value': choice[0], 'display_name': choice[1]} for choice in UNIT_CHOICES]
    serializer = UnitChoicesSerializer(choices, many=True)
    response_data = {
        "status_code" :200,
        "title" : "Units",
        "data" : serializer.data
    }
    return Response(response_data, status=status.HTTP_200_OK)


# contributor crud starts here
@api_view(["POST"])
@permission_classes([IsAuthenticated])
def create_contributor(request):
    data = request.data
    email = data.get("email")
    password = data.get("password")
    first_name = data.get("first_name")
    last_name = data.get("last_name")

    if not (email and password and first_name and last_name):
        return Response({
            "status": 400,
            "message": "Email, password, first name, and last name are required."
        }, status=status.HTTP_400_BAD_REQUEST)

    if CustomUser.objects.filter(email=email).exists():
        return Response({
            "status": 400,
            "message": "User with this email already exists."
        }, status=status.HTTP_400_BAD_REQUEST)

    try:
        contributor_role = Role.objects.get(name="contributor")
    except Role.DoesNotExist:
        return Response({
            "status": 400,
            "message": "Contributor role does not exist. Please create the role first."
        }, status=status.HTTP_400_BAD_REQUEST)

    user = CustomUser.objects.create_user(
        email=email,
        password=password,
        first_name=first_name,
        last_name=last_name,
        is_active=True,
        is_staff=False,
        is_registered=True,
        is_verified=True
    )

    user.roles.add(contributor_role)

    contributor_data = {
        "user": user.id,
        "creator": request.user.id,  # Ensure you use user ID
        "updator": request.user.id
    }

    contributor_serializer = ContributorCreateSerializer(data=contributor_data)
    if contributor_serializer.is_valid():
        contributor_serializer.save()
    else:
        return Response({
            "status": 400,
            "message": "Error creating contributor profile",
            "errors": contributor_serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)

    response_data = {
        "status": 201,
        "message": "Contributor created successfully. They can log in and update their details.",
        "user": UserSerializer(user).data,
        "contributor": contributor_serializer.data
    }

    return Response(response_data, status=status.HTTP_201_CREATED)



@api_view(["GET"])
def contributors(request):
    instances = Contributor.objects.filter(is_deleted=False)
    paginator = StandardResultSetPagination()
    paginated_contributors = paginator.paginate_queryset(instances, request)
    serializer = ContributorSerializer(paginated_contributors, many=True)    
    response_data = {
        "status": 200,
        "message": "Contributors List",
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
def edit_contributor(request, pk):
    instance = get_object_or_404(Contributor.objects.filter(pk=pk, is_deleted=False))
    serializer = ContributorSerializer(instance=instance, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save(updator=request.user, date_updated=timezone.now())
        response_data = {
            "status":"true",
            "redirect":"true",
            "title":"Successfully Updated",
            "data":serializer.data,
            "message":"Contributor Updated Successfully",
            "redirect_url":reverse('contributor_api:contributors')
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
def contributor(request, pk):
    instance = get_object_or_404(Contributor.objects.filter(pk=pk,is_deleted=False))
    serializer = ContributorSerializer(instance)
    response_data = {
        "status_code" :200,
        "title" : "Contributor Details",
        "data" : serializer.data
    }
    return Response(response_data)


@api_view(["PUT"])
def delete_contributor(request,pk):
    instance = get_object_or_404(Contributor.objects.filter(pk=pk,is_deleted=False))  
    Contributor.objects.filter(pk=pk).update(is_deleted=True)    
    response_data = {
        "status" : 200,        
        "title" : "Successfully Deleted",
        "message" : "Contributor Successfully Deleted.", 
        "redirect" : "true",       
        "redirect_url" : reverse('contributor_api:contributors')
    }
    return Response(response_data)


# task crud starts here
@api_view(["POST"])
# @permission_classes([IsAuthenticated])
def create_task(request):   
    serializer = TaskSerializer(data=request.data)
    if serializer.is_valid():
        print("task serializer is valid")
        name = serializer.validated_data['name']
        weightage = serializer.validated_data['weightage']
        unit = serializer.validated_data['unit']
        creator = request.user
        updator = request.user
        print("task name ",name)
        if not Task.objects.filter(name=name).exists():
            Task(                    
                name = name, 
                weightage = weightage,
                unit = unit,
                creator = creator,
                updator = updator
            ).save()
            print("task is saved")
            response_data = {
                "status": 200,
                "title": "Successfully Created",
                "message": "Task created successfully.",
                "data":serializer.data,
                "redirect": "true"
            }
        else:
            print("errors ",serializer.errors)
            response_data = {
                "status": 400,
                "stable": "true",
                "error":serializer.errors,
                "title": "Already exists",
                "message": "Task already exists",                        
            }
    else:
        print("errors ",serializer.errors)    
        response_data = {
            "stable": "true",
            "status": 400,
            "error":serializer.errors,
            "title": "Form validation error",
            "message": "Validation Error",               
        }
    return Response(response_data)


@api_view(["GET"])
def tasks(request):
    instances = Task.objects.filter(is_deleted=False)
    paginator = StandardResultSetPagination()
    paginated_tasks = paginator.paginate_queryset(instances, request)
    serializer = TaskSerializer(paginated_tasks, many=True)    
    response_data = {
        "status": 200,
        "message": "Tasks List",
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
@permission_classes([IsAuthenticated])
def edit_task(request, pk):
    instance = get_object_or_404(Task.objects.filter(pk=pk, is_deleted=False))
    serializer = TaskSerializer(instance=instance, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save(updator=request.user, date_updated=timezone.now())
        response_data = {
            "status":"true",
            "redirect":"true",
            "title":"Successfully Updated",
            "data":serializer.data,
            "message":"Task Updated Successfully"
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
def task(request, pk):
    instance = get_object_or_404(Task.objects.filter(pk=pk, is_deleted=False))
    serializer = TaskSerializer(instance)
    response_data = {
        "status_code": 200,
        "title": "Task Details",
        "data": serializer.data
    }
    return Response(response_data)


@api_view(["PUT"])
@permission_classes([IsAuthenticated])
def delete_task(request,pk):
    instance = get_object_or_404(Task.objects.filter(pk=pk,is_deleted=False))  
    Task.objects.filter(pk=pk).update(is_deleted=True,title=instance.title + "_deleted_" )    
    response_data = {
        "status" : 200,        
        "title" : "Successfully Deleted",
        "message" : "Task Successfully Deleted.", 
        "redirect" : "true"
    }
    return Response(response_data)

# job crud starts here
@api_view(["POST"])
# @permission_classes([IsAuthenticated])
def create_contributor_task(request):   
    serializer = ContributorTaskSerializer(data=request.data)
    if serializer.is_valid():
        contributor = serializer.validated_data['contributor']
        task = serializer.validated_data['task']
        status = serializer.validated_data['status']
        weightage_after_deadline = serializer.validated_data['weightage_after_deadline']
        first_deadline = serializer.validated_data['first_deadline']
        second_deadline = serializer.validated_data['second_deadline']
        net_weightage = serializer.validated_data['net_weightage']
        creator = request.user
        updator = request.user

        if not ContributorTask.objects.filter(task=task).exists():
            ContributorTask(                    
                contributor = contributor, 
                task = task,
                status = status, 
                weightage_after_deadline = weightage_after_deadline, 
                first_deadline = first_deadline, 
                second_deadline = second_deadline,
                net_weightage = net_weightage,
                creator = creator,
                updator = updator
            ).save()
            response_data = {
                "status": 200,
                "title": "Successfully Created",
                "message": "Contributor Task created successfully.",
                "data":serializer.data,
                "redirect": "true"
            }
        else:            
            response_data = {
                "status": 400,
                "stable": "true",
                "error":serializer.errors,
                "title": "Already exists",
                "message": "Contributor Task already exists",                        
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
def contributor_tasks(request):
    instances = ContributorTask.objects.filter(is_deleted=False)
    paginator = StandardResultSetPagination()
    paginated_contributor_tasks = paginator.paginate_queryset(instances, request)
    serializer = ContributorTaskSerializer(paginated_contributor_tasks, many=True)    
    response_data = {
        "status": 200,
        "message": "Contributor Tasks List",
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
@permission_classes([IsAuthenticated])
def edit_contributor_task(request, pk):
    instance = get_object_or_404(ContributorTask.objects.filter(pk=pk, is_deleted=False))
    serializer = ContributorTaskSerializer(instance=instance, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save(updator=request.user, date_updated=timezone.now())
        response_data = {
            "status":"true",
            "redirect":"true",
            "title":"Successfully Updated",
            "data":serializer.data,
            "message":"Contributor Task Updated Successfully"
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
def contributor_task(request, pk):
    instance = get_object_or_404(ContributorTask.objects.filter(pk=pk, is_deleted=False))
    serializer = ContributorTaskSerializer(instance)
    response_data = {
        "status_code": 200,
        "title": "Contributor Task Details",
        "data": serializer.data
    }
    return Response(response_data)


@api_view(["PUT"])
@permission_classes([IsAuthenticated,])
def delete_contributor_task(request,pk):
    instance = get_object_or_404(ContributorTask.objects.filter(pk=pk,is_deleted=False))  
    ContributorTask.objects.filter(pk=pk).update(is_deleted=True,title=instance.title + "_deleted_" )    
    response_data = {
        "status" : 200,        
        "title" : "Successfully Deleted",
        "message" : "Contributor Task Successfully Deleted.", 
        "redirect" : "true"
    }
    return Response(response_data)


@api_view(['GET'])
def contributor_task_summary(request):
    tasks = ContributorTask.objects.select_related('contributor', 'task', 'contributor__user').all()
    
    contributors = {}
    
    # Prepare the data in a nested structure
    for task in tasks:
        contributor_name = f"{task.contributor.user.first_name} {task.contributor.user.last_name}"
        if contributor_name not in contributors:
            contributors[contributor_name] = {
                'Initial Percentage': 20,  # Placeholder for initial percentage, can be dynamic
                'Tasks': []
            }
        
        # Serialize the task data using the serializer
        task_data = ContributorTaskSerializer(task).data
        contributors[contributor_name]['Tasks'].append(task_data)
    
    return Response(contributors)

