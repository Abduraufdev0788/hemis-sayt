from django.db import models

class Group(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name
    

class GroupSubject(models.Model):
    group = models.ForeignKey("groups.Group", on_delete=models.CASCADE)
    subject = models.ForeignKey("subjects.Subject", on_delete=models.CASCADE)


    class Meta:
        unique_together = ['group', 'subject']

    def __str__(self):
        return f"{self.group} - {self.subject}"