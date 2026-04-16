from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404

from users.models import Children
from subjects.models import Teacher
from users.permissions import IsTeacher
from groups.models import Group

from .serializers import TeacherStudentSerializer, TeacherProfileSerializers


class TeacherStudentsView(APIView):
    permission_classes = [IsAuthenticated, IsTeacher]

    def get(self, request):
        group_id = request.GET.get("group_id")

        students = Children.objects.filter(
            group_id=group_id,
            role="student" 
        )

        data = [
            {
                "id": s.id,
                "first_name": s.first_name,
                "last_name": s.last_name,
                "absent_hours": s.total_absent_hours
            }
            for s in students
        ]

        print("STUDENTS:", data)

        return Response({
            "students": data
        })

# 🔥 2. STATS
class TeacherStatsView(APIView):
    permission_classes = [IsAuthenticated, IsTeacher]

    def get(self, request):
        teacher = get_object_or_404(Teacher, user=request.user)

        students_count = Children.objects.filter(role = "student")
        groups_count = Group.objects.all()

        return Response({
            "groups": groups_count.count(),
            "students": students_count.count(),
            "subject": teacher.subject.name
        })


# 🔥 3. PROFILE
class TeacherProfileView(APIView):
    permission_classes = [IsAuthenticated, IsTeacher]

    def get(self, request):
        teacher = get_object_or_404(Teacher, user=request.user)

        serializer = TeacherProfileSerializers(teacher)

        print(serializer.data)

        return Response(serializer.data)

    
    
class TeacherGroupsView(APIView):
    permission_classes = [IsAuthenticated, IsTeacher]

    def get(self, request):

        groups = Group.objects.all()

        data = [
            {
                "id": g.id,
                "name": g.name
            }
            for g in groups
        ]

        return Response(data)