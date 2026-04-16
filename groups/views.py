from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from users.models import Children
from subjects.models import Teacher
from users.permissions import IsTeacher

class GroupStudentsView(APIView):
    permission_classes = [IsAuthenticated, IsTeacher]

    def get(self, request, group_id):
        teacher = get_object_or_404(Teacher, user=request.user)

        if not teacher.groups.filter(id=group_id).exists():
            return Response({"error": "Ruxsat yo‘q"}, status=403)

        students = Children.objects.filter(group_id=group_id)

        data = [
            {
                "id": s.id,
                "first_name": s.first_name,
                "last_name": s.last_name
            }
            for s in students
        ]

        return Response(data)