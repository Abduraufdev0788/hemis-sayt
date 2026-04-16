from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.db.models import Sum

from users.models import Children
from users.permissions import IsTeacher
from .models import Attendance
from .utils import send_telegram
from django.db.models import Count

from datetime import date, datetime


class AttendanceView(APIView):
    permission_classes = [IsAuthenticated, IsTeacher]  # 🔥 qo‘shildi

    def get(self, request):
        group_id = request.GET.get("group_id")
        date = request.GET.get("date")

        attendance = Attendance.objects.filter(
            group_id=group_id,
            date=date
        )

        data = {
            a.student.id: a.status
            for a in attendance
        }

        return Response(data)

    def post(self, request):
        data = request.data
        date = datetime.strptime(data.get("date"), "%Y-%m-%d").date()

        for item in data.get("students", []):
            student = Children.objects.get(id=item["student_id"])
            status = item["status"]
            parent = student.parent

            existing = Attendance.objects.filter(
                student=student,
                group_id=item["group_id"],
                date=date
            ).first()

            # 🔥 AGAR OLDIN YOZILGAN BO‘LSA
            if existing:
                old_status = existing.status

                # ❌ NB → ✔ present
                if old_status == "absent" and status == "present":
                    student.total_absent_hours = max(0, student.total_absent_hours - 2)
                    student.save()

                # ✔ present → ❌ NB
                elif old_status != "absent" and status == "absent":
                    student.total_absent_hours += 2
                    student.save()

                    # 🔥 TELEGRAM: bugun kelmadi
                    if parent and parent.telegram_id:
                        send_telegram(
                            parent.telegram_id,
                            f"""❌ Farzandingiz bugun darsga kelmadi!

                                👤 {student.first_name} {student.last_name}
                                📚 Guruh: {student.group.name}
                                📅 Sana: {date}

                                ⏱ Jami qoldirgan soati: {student.total_absent_hours}
                                """
                                                    )

                        # 🔥 10+ OGOLANTIRISH (FAKAT 1 MARTA)
                        if 10 <= student.total_absent_hours < 12:
                            send_telegram(
                                parent.telegram_id,
                                f"⚠️ Diqqat! {student.first_name} 10 soatdan ko‘p dars qoldirdi!"
                            )

                existing.status = status
                existing.save()

            # 🔥 AGAR YANGI YOZUV BO‘LSA
            else:
                Attendance.objects.create(
                    student=student,
                    group_id=item["group_id"],
                    date=date,
                    status=status
                )

                if status == "absent":
                    student.total_absent_hours += 2
                    student.save()

                    if parent and parent.telegram_id:
                        send_telegram(
                            parent.telegram_id,
                            f"""❌ Farzandingiz bugun darsga kelmadi!

👤 {student.first_name} {student.last_name}
📚 Guruh: {student.group.name}
📅 Sana: {date}

⏱ Jami qoldirgan soati: {student.total_absent_hours}
"""
                    )

                        if 10 <= student.total_absent_hours < 12:
                            send_telegram(
                                parent.telegram_id,
                                f"⚠️ Diqqat! {student.first_name} 10 soatdan ko‘p dars qoldirdi!"
                            )

        return Response({"success": True})
    


class StudentNBView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        student = request.user

        total_nb = student.total_absent_hours

        # 🔥 STATUS HISOBLASH
        if total_nb >= 20:
            status_text = "🚨 Xavf"
        elif total_nb >= 10:
            status_text = "⚠️ Ogohlantirish"
        else:
            status_text = "✅ Yaxshi"

        return Response({
            "total_nb": total_nb,
            "status_text": status_text
        })
    
class StudentTodayStatusView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        student = request.user
        today = date.today()

        today_att = Attendance.objects.filter(
            student=student,
            date=today
        ).first()

        last_att = Attendance.objects.filter(
            student=student
        ).order_by("-date").first()

        return Response({
            "today_status": today_att.status if today_att else None,
            "last_status": last_att.status if last_att else None,
            "last_date": last_att.date if last_att else None
        })
    

class StudentRankingView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        student = request.user

        group_students = Children.objects.filter(group=student.group)

        # 🔥 sort (kam NB yaxshi)
        sorted_students = sorted(
            group_students,
            key=lambda x: x.total_absent_hours
        )

        rank = next(i+1 for i, s in enumerate(sorted_students) if s.id == student.id)

        return Response({
            "rank": rank,
            "total_students": len(sorted_students)
        })