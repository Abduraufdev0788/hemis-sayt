from rest_framework import serializers
from users.models import Children
from .models import Teacher
from groups.models import Group
from .models import Subject
from django.contrib.auth.hashers import make_password


class TeacherRegisterSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()
    subject_id = serializers.IntegerField()
    group_id = serializers.IntegerField()

    def create(self, validated_data):

        user = Children.objects.create(
            username=validated_data['username'],
            password=make_password(validated_data['password'])
        )

        subject = Subject.objects.get(id=validated_data['subject_id'])
        group = Group.objects.get(id=validated_data['group_id'])

        teacher = Teacher.objects.create(
            user=user,
            subject=subject,
            group=group
        )

        return teacher