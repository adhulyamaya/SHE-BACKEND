from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework import status
from market.models import ProjectSeller, MarketplaceProject, Order
from user.models import Role
from .serializers import ProjectSellerSerializer, SellerCreateSerializer, MarketplaceProjectSerializer, MarketplaceProjectCreateSerializer, OrderSerializer
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
import razorpay
from django.conf import settings


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def projectseller_list(request):
    projectsellers = ProjectSeller.objects.filter(is_deleted=False)
    serializer = ProjectSellerSerializer(projectsellers, many=True)
    
    response_data = {
        "status": 200,
        "data": serializer.data,
        "message": "Project sellers retrieved successfully."
    }
    return Response(response_data)

@api_view(["POST"])
@permission_classes([IsAuthenticated])
def projectseller_create(request):
    data = request.data
    print(data)
    user = request.user  # Get the authenticated user
    country = data.get("country")
    state = data.get("state")
    phone = data.get("phone")
    bio = data.get("bio", "")
    git_hub = data.get("git_hub", "")
    linked_in = data.get("linked_in", "")
    skills = data.get("skills", "")
    photo = request.FILES.get("photo", None)

    # Validate required fields
    if not (country and state):
        return Response({
            "status": 400,
            "message": "Country and state are required."
        }, status=status.HTTP_400_BAD_REQUEST)

    # Retrieve seller role (if necessary for your logic)
    try:
        seller_role = Role.objects.get(name="project_seller")
    except Role.DoesNotExist:
        return Response({
            "status": 400,
            "message": "Seller role does not exist. Please create the role first."
        }, status=status.HTTP_400_BAD_REQUEST)

    # Prepare seller data
    seller_data = {
        "user": user.id,  # Using the authenticated user
        "country": country,
        "state": state,
        "bio": bio,
        "phone": phone,
        "git_hub": git_hub,
        "linked_in": linked_in,
        "skills": skills,
        "photo": photo,
        "creator": user.id,  # Assuming you store the creator of the seller
        "updator": user.id   # Assuming you store the updator
    }

    # Serialize seller data
    seller_serializer = SellerCreateSerializer(data=seller_data)
    if seller_serializer.is_valid():
        seller_serializer.save()
    else:
        return Response({
            "status": 400,
            "message": "Error creating seller profile",
            "errors": seller_serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)

    # Response with success
    response_data = {
        "status": 201,
        "message": "Seller created successfully. They can log in and update their details.",
        "seller": seller_serializer.data
    }

    return Response(response_data, status=status.HTTP_201_CREATED)

@api_view(["GET"])
@permission_classes([IsAuthenticated])
def projectseller_detail(request):
    try:
        instance = get_object_or_404(ProjectSeller.objects.filter(user=request.user,is_deleted=False))
        serializer = ProjectSellerSerializer(instance)
        response_data = {
            "status_code" :200,
            "title" : "Companion Details",
            "data" : serializer.data
        }
        return Response(response_data)

    except ProjectSeller.DoesNotExist:
        return Response({
            "status": 404,
            "message": "Seller not found."
        }, status=status.HTTP_404_NOT_FOUND)

    except Exception as e:
        return Response({
            "status": 500,
            "message": "An error occurred.",
            "error": str(e)
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def projectseller_update(request):
    user = request.user
    print("User:", user)
    print("Request Data:", request.data)

    # Check for file upload
    if 'photo' in request.FILES:
        print("Photo file:", request.FILES['photo'])
    else:
        print("No photo file uploaded.")

    projectseller = get_object_or_404(ProjectSeller, user=user, is_deleted=False)
    serializer = ProjectSellerSerializer(projectseller, data=request.data, partial=True)
    
    if serializer.is_valid():
        serializer.save()
        response_data = {
            "status": 200,
            "title": "Successfully Updated",
            "data": serializer.data,
            "message": "Project seller updated successfully.",
            "redirect": "true"
        }
        return Response(response_data)
    else:
        print("Validation Errors:", serializer.errors)
        response_data = {
            "stable": "true",
            "status": 400,
            "error": serializer.errors,
            "title": "Form validation error",
            "message": "Validation Error"
        }
        return Response(response_data)

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def projectseller_delete(request, pk):
    projectseller = get_object_or_404(ProjectSeller, pk=pk, is_deleted=False)
    projectseller.is_deleted = True  # Perform soft delete
    projectseller.save()
    
    response_data = {
        "status": 200,
        "message": "Project seller deleted successfully."
    }
    return Response(response_data)


@api_view(['GET'])
@permission_classes([AllowAny])
def marketplace_projects(request):
    projects = MarketplaceProject.objects.filter(is_deleted=False)
    serializer = MarketplaceProjectSerializer(projects, many=True)
    return Response({
        "status": 200,
        "data": serializer.data,
        "message": "Marketplace projects retrieved successfully."
    })

@api_view(["POST"])
@permission_classes([IsAuthenticated])
def create_marketplace_project(request):
    # Get the user from the request
    user = request.user
    seller = ProjectSeller.objects.get(user=user)
    print(seller)

    print(request.data)

    # Prepare the project data from the request
    project_data = {
        'seller': seller.id,  # Assuming the seller is the authenticated user
        'title': request.data.get('title'),
        'description': request.data.get('description'),
        'price': request.data.get('price'),
        'video_url': request.data.get('video_url'),
        'image': request.FILES.get('image'),  # Handle file uploads
        'tech_stack': request.data.get('tech_stack'),
        'demo_link': request.data.get('demo_link'),
        'is_sold': request.data.get('is_sold', False),
        'is_verified': request.data.get('is_verified', False),
        'is_deleted': request.data.get('is_deleted', False),
        'creator' : user.id, 
        'updator' : user.id
    }


    # Serialize the project data
    serializer = MarketplaceProjectCreateSerializer(data=project_data)
    if serializer.is_valid():
        serializer.save()
        response_data = {
            "status": 201,
            "message": "Marketplace project created successfully.",
            "data": serializer.data,
        }
        return Response(response_data, status=status.HTTP_201_CREATED)
    else:
        return Response({
            "status": 400,
            "error": serializer.errors,
            "message": "Validation error.",
        }, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@permission_classes([AllowAny])
def view_marketplace_project(request, pk):
    try:
        project = MarketplaceProject.objects.get(pk=pk)
        serializer = MarketplaceProjectSerializer(project)
        return Response({
            "status": 200,
            "data": serializer.data,
            "message": "Marketplace project retrieved successfully."
        })
    except MarketplaceProject.DoesNotExist:
        return Response({
            "status": 404,
            "message": "Marketplace project not found."
        }, status=status.HTTP_404_NOT_FOUND)

@api_view(['GET'])
def seller_marketplace_projects(request):
    # Ensure the user is authenticated
    if not request.user.is_authenticated:
        return Response({
            "status": 401,
            "message": "Authentication required"
        }, status=status.HTTP_401_UNAUTHORIZED)
    
    # Fetch the seller object associated with the current user
    try:
        seller = ProjectSeller.objects.get(user=request.user)
    except ProjectSeller.DoesNotExist:
        return Response({
            "status": 404,
            "message": "Seller profile not found for this user"
        }, status=status.HTTP_404_NOT_FOUND)

    # Fetch all marketplace projects for this seller
    projects = MarketplaceProject.objects.filter(seller=seller, is_deleted=False)
    
    # Serialize the projects data
    serializer = MarketplaceProjectSerializer(projects, many=True)

    return Response({
        "status": 200,
        "data": serializer.data,
        "message": "Seller's marketplace projects retrieved successfully."
    }, status=status.HTTP_200_OK)

@api_view(['PUT'])
def edit_marketplace_project(request, pk):
    try:
        project = MarketplaceProject.objects.get(pk=pk)

        # Prepare the data, including files
        data = request.data.copy()

        # Handle file uploads separately
        if 'image' in request.FILES:
            data['image'] = request.FILES['image']

        # Use partial update to allow updating only specific fields
        serializer = MarketplaceProjectSerializer(project, data=data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response({
                "status": 200,
                "title": "Successfully Updated",
                "data": serializer.data,
                "message": "Marketplace project updated successfully."
            })
        else:
            return Response({
                "status": 400,
                "error": serializer.errors,
                "title": "Form validation error",
                "message": "Validation Error",
            }, status=status.HTTP_400_BAD_REQUEST)
    
    except MarketplaceProject.DoesNotExist:
        return Response({
            "status": 404,
            "message": "Marketplace project not found."
        }, status=status.HTTP_404_NOT_FOUND)

@api_view(['PUT'])
def delete_marketplace_project(request, pk):
    try:
        project = MarketplaceProject.objects.get(pk=pk)
        instance = get_object_or_404(MarketplaceProject.objects.filter(pk=pk,is_deleted=False))  
        MarketplaceProject.objects.filter(pk=pk).update(is_deleted=True) 
        return Response({
            "status": 204,
            "message": "Marketplace project deleted successfully."
        }, status=status.HTTP_204_NO_CONTENT)
    except MarketplaceProject.DoesNotExist:
        return Response({
            "status": 404,
            "message": "Marketplace project not found."
        }, status=status.HTTP_404_NOT_FOUND)
    
razorpay_client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))

class CreateOrderView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        project_id = request.data.get('project_id')
        project = get_object_or_404(MarketplaceProject, id=project_id)

        if project.is_sold:
            return Response({"error": "This project has already been sold."}, status=status.HTTP_400_BAD_REQUEST)

        amount = int(project.price * 100)  # Razorpay expects amount in paise
        currency = "INR"
        
        razorpay_order = razorpay_client.order.create(dict(
            amount=amount,
            currency=currency,
            payment_capture='0'
        ))

        order = Order.objects.create(
            user=request.user,
            project=project,
            razorpay_order_id=razorpay_order['id'],
            amount=amount,
        )

        serializer = OrderSerializer(order)
        
        data = {
            "order_id": razorpay_order['id'],
            "currency": currency,
            "amount": amount,
            "key": settings.RAZORPAY_KEY_ID,
            "order_details": serializer.data,
        }
        return Response({"data": data}, status=status.HTTP_200_OK)

class VerifyPaymentView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        razorpay_payment_id = request.data.get('razorpay_payment_id')
        razorpay_order_id = request.data.get('razorpay_order_id')
        razorpay_signature = request.data.get('razorpay_signature')

        order = get_object_or_404(Order, razorpay_order_id=razorpay_order_id)

        # Verify the payment signature
        params_dict = {
            'razorpay_order_id': razorpay_order_id,
            'razorpay_payment_id': razorpay_payment_id,
            'razorpay_signature': razorpay_signature
        }

        try:
            razorpay_client.utility.verify_payment_signature(params_dict)
        except:
            return Response({"error": "Invalid payment signature"}, status=status.HTTP_400_BAD_REQUEST)

        # Capture the payment
        razorpay_client.payment.capture(razorpay_payment_id, order.amount)

        # Update the order
        order.is_paid = True
        order.razorpay_payment_id = razorpay_payment_id
        order.save()

        # Update the project as sold
        order.project.is_sold = True
        order.project.save()

        return Response({"data": {"success": True, "message": "Payment successful"}}, status=status.HTTP_200_OK)

class PurchaseHistoryView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        orders = Order.objects.filter(user=request.user, is_paid=True)
        serializer = OrderSerializer(orders, many=True)
        return Response({"data": serializer.data}, status=status.HTTP_200_OK)
