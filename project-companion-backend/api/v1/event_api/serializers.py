from rest_framework.serializers import ModelSerializer
from event.models import Event, EventRegistration,CustomUser


class UserSerializer(ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['first_name','last_name','email','roles']
        
class EventSerializer(ModelSerializer):
    user = UserSerializer(read_only = True)
    organizer = UserSerializer(read_only=True)
    class Meta:
        model = Event
        exclude = ['creator', 'updator', 'is_deleted','is_completed']
        read_only_fields = ['user', 'organizer']

class EventRegistrationSerializer(ModelSerializer):
    event_details = EventSerializer(read_only=True, source='event')
    class Meta:
        model = EventRegistration
        fields = ['id', 'user', 'event', 'event_details', 'registration_date', 'is_cancel']
        # exclude = ['creator', 'updator', 'is_attended','is_cancel']
        read_only_fields = ['user','registration_date', 'is_cancel']
