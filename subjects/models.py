from django.db import models

class Subject(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name
    

class Teacher(models.Model):
    user = models.OneToOneField("users.Children", on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user.username} - {self.subject.name}"