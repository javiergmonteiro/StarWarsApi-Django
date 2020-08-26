from .models import Character_Rating
from rest_framework import serializers

class Character_Rating_Serializer(serializers.ModelSerializer):

    class Meta:
        model = Character_Rating
        fields = ['character','rating']

    def create(self,validated_data):
        obj = Character_Rating.objects.create(**validated_data)
        obj.save()
        return obj

