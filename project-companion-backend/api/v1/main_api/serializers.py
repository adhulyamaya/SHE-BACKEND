from rest_framework.serializers import ModelSerializer
from main.models import Country, State


class CountrySerializer(ModelSerializer):
    class Meta:
        model = Country
        fields = '__all__'



class StateSerializer(ModelSerializer):
    country = CountrySerializer()
    class Meta:
        model = State
        fields = '__all__'