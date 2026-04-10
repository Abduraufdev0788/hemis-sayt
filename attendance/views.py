from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Attendance
from users.models import Children
from subjects.models import Teacher
from groups.models import GroupSubject
from .utils import check_nb
from django.db.models import Sum


from rest_framework import status
from django.shortcuts import get_object_or_404
from users.permissions import IsTeacher, IsStudent
from .serializers import AttendanceSerializer

class AddAttendanceView(APIView):
    permission_classes = [IsAuthenticated, IsTeacher]

    def post(self, request):
        teacher = get_object_or_404(Teacher, user=request.user)

        serializer = AttendanceSerializer(data=request.data)

        if serializer.is_valid():
            student = serializer.validated_data['student']

            # 🔥 GROUP CHECK
            if teacher.group != student.group:
                return Response({"error": "Bu student sizning guruhingiz emas"}, status=403)

            # 🔥 SUBJECT CHECK
            if not GroupSubject.objects.filter(
                group=student.group,
                subject=teacher.subject
            ).exists():
                return Response({"error": "Bu fan bu guruhda yo‘q"}, status=403)

            # 🔥 SAVE
            Attendance.objects.create(
                student=student,
                subject=teacher.subject,
                hours=serializer.validated_data['hours']
            )

            check_nb(student)

            return Response({"success": True}, status=201)

        return Response(serializer.errors, status=400)
    



class StudentNBView(APIView):
    permission_classes = [IsAuthenticated, IsStudent]

    def get(self, request):
        student = request.user

        total = Attendance.objects.filter(student=student).aggregate(
            Sum('hours')
        )['hours__sum'] or 0

        subjects = Attendance.objects.filter(student=student).values(
            'subject__name'
        ).annotate(total=Sum('hours'))

        return Response({
            "total_nb": total,
            "subjects": subjects
        })