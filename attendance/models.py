from django.db import models
from users.models import Children
from groups.models import Group

class Attendance(models.Model):
    student = models.ForeignKey(Children, on_delete=models.CASCADE)
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    date = models.DateField()

    STATUS_CHOICES = (
        ("present", "Kelgan"),
        ("absent", "NB"),
    )

    status = models.CharField(max_length=10, choices=STATUS_CHOICES)

    class Meta:
        unique_together = ("student", "group", "date")  # 🔥 duplicate yo‘q

    def __str__(self):
        return f"{self.student} - {self.date} - {self.status}"