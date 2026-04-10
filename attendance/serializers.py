from rest_framework import serializers
from .models import Attendance


class AttendanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Attendance
        fields = ["student", "hours"]  # subjectni viewda beramiz

    def validate_hours(self, value):
        if value <= 0:
            raise serializers.ValidationError("hours > 0 bo‘lishi kerak")
        return value