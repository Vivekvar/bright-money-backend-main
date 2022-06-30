from rest_framework import serializers
from .models import client, item

#Serializer for Client Model

class ClientSerializer(serializers.ModelSerializer):
    class Meta:
        model = client
        fields = '__all__'
        extra_kwargs = {
            'password': {'write_only': True}
        }


#Serializer for Item Model
class ItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = item
        fields = '__all__'