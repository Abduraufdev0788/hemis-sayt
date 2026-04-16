from django.db import models
from core.settings import AUTH_USER_MODEL
from groups.models import Group

class Subject(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name
    

class Teacher(models.Model):
    subject = models.ForeignKey("subjects.Subject", related_name="teachers", on_delete=models.CASCADE)
    user = models.OneToOneField(AUTH_USER_MODEL, on_delete=models.CASCADE) 
    groups = models.ManyToManyField(Group, related_name="teachers",  null=True, blank=True)


    def __str__(self):
        return f"{self.user} - {self.subject}"