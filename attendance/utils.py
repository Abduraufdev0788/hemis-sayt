from django.db.models import Sum
from .models import Attendance


def get_total_nb(student):
    return Attendance.objects.filter(student=student).aggregate(
        Sum('hours')
    )['hours__sum'] or 0


def get_subject_nb(student):
    return Attendance.objects.filter(student=student).values(
        'subject__name'
    ).annotate(total=Sum('hours'))

import requests

def send_telegram(chat_id):
    token = "BOT_TOKEN"

    requests.post(
        f"https://api.telegram.org/bot{token}/sendMessage",
        data={
            "chat_id": chat_id,
            "text": "Farzandingiz 10 soatdan ko‘p dars qoldirdi!"
        }
    )


def check_nb(student):
    total = get_total_nb(student)

    if total >= 10:
        send_telegram(student.parent.telegram_id)