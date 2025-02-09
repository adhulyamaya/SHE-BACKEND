from rest_framework import serializers
from market.models import ProjectSeller, MarketplaceProject, Order

class ProjectSellerSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProjectSeller
        fields = [
            'user', 'photo', 'bio', 'phone',
            'git_hub', 'linked_in', 'skills', 'is_deleted', 'is_blocked', 'country', 'state'
        ]

class SellerCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProjectSeller
        fields = ['user', 'country', 'state', 'bio', 'phone', 'git_hub', 'linked_in', 'skills', 'photo', 'creator', 'updator']

class MarketplaceProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = MarketplaceProject
        fields = [
            'id', 'seller', 'title', 'description', 'price',
            'video_url', 'image', 'tech_stack', 'demo_link',
            'is_sold', 'is_verified', 'is_deleted'
        ]

class MarketplaceProjectCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = MarketplaceProject
        fields = [
            'seller',
            'title',
            'description',
            'price',
            'video_url',
            'image',
            'tech_stack',
            'demo_link',
            'is_sold',
            'is_verified',
            'is_deleted',
            'creator',
            'updator'
        ]
        extra_kwargs = {
            'is_sold': {'default': False},
            'is_verified': {'default': False},
            'is_deleted': {'default': False},
        }

    def validate(self, data):
        """
        Validate the input data.
        """
        if data['price'] <= 0:
            raise serializers.ValidationError("Price must be greater than zero.")
        if not data.get('tech_stack'):
            raise serializers.ValidationError("Tech stack is required.")
        # Additional validation can be added here if needed

        return data
    
class OrderSerializer(serializers.ModelSerializer):
    project_title = serializers.CharField(source='project.title', read_only=True)

    class Meta:
        model = Order
        fields = ['id', 'user', 'project', 'project_title', 'amount', 'is_paid', 'razorpay_order_id', 'razorpay_payment_id', 'created_at']
        read_only_fields = ['user', 'project', 'amount', 'is_paid', 'razorpay_order_id', 'razorpay_payment_id', 'created_at']