from rest_framework import serializers
from subjects.models import Teacher
from users.models import Children


class TeacherStudentSerializer(serializers.ModelSerializer):
    group = serializers.CharField(source="group.name", read_only=True)

    class Meta:
        model = Children
        fields = ["id", "first_name", "last_name", "group"]

class TeacherProfileSerializers(serializers.ModelSerializer):
    first_name = serializers.CharField(source="user.first_name")
    last_name = serializers.CharField(source="user.last_name")
    username = serializers.CharField(source="user.username")

    subject = serializers.CharField(source="subject.name")
    groups = serializers.SerializerMethodField()

    class Meta:
        model = Teacher
        fields = [
            "username",
            "first_name",
            "last_name",
            "subject",
            "groups"
        ]

    def get_groups(self, obj):
        return [obj.groups.count()]