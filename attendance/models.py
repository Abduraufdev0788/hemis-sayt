from django.db import models

class Attendance(models.Model):
    student = models.ForeignKey("users.Children", on_delete=models.CASCADE)
    subject = models.ForeignKey("subjects.Subject", on_delete=models.CASCADE)
    hours = models.IntegerField()
    date = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.student.username} - {self.subject.name} - {self.hours}"