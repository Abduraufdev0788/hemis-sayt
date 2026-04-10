from rest_framework import serializers
from .models import Children, Parents
from django.contrib.auth.hashers import check_password

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
    

class ChildrenSerializer(serializers.ModelSerializer):
    parent_phone = serializers.CharField(write_only=True)

    class Meta:
        model = Children
        fields = [
            'first_name',
            'last_name',
            'email',
            'username',
            'password',
            'parent_phone'
        ]

    def create(self, validated_data):
        parent_phone = validated_data.pop('parent_phone')

        try:
            parent = Parents.objects.get(phone_number=parent_phone)
        except Parents.DoesNotExist:
            raise serializers.ValidationError({
                "parent_phone": "Bunday parent topilmadi"
            })


        from django.contrib.auth.hashers import make_password
        validated_data['password'] = make_password(validated_data['password'])

        child = Children.objects.create(parent=parent, **validated_data)

        return child
    

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()

    def validate(self, data):
        username = data.get("username")
        password = data.get("password")

        try:
            user = Children.objects.get(username=username)
        except Children.DoesNotExist:
            raise serializers.ValidationError("User topilmadi")

        if not check_password(password, user.password):
            raise serializers.ValidationError("Parol noto‘g‘ri")

        data['user'] = user
        return data