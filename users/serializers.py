from rest_framework import serializers
from .models import Parents

class ParentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Parents
        fields = ['telegram_id', 'phone_number', 'name']

    def create(self, validated_data):
        print(validated_data)
        parent, created = Parents.objects.update_or_create(
            telegram_id=validated_data['telegram_id'],
            name=validated_data['name'],
            phone_number=validated_data['phone_number']
        )
        return parent