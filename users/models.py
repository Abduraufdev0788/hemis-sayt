from django.db import models

class Parents(models.Model):
    telegram_id = models.BigIntegerField(unique=True)
    phone_number = models.CharField(max_length=20)
    name = models.CharField(max_length=255)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} ({self.telegram_id})"

class  Children(models.Model):
    parent = models.ForeignKey(Parents, on_delete=models.CASCADE, related_name='children')
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.EmailField(blank=True, null=True)
    username = models.CharField(max_length=255 , unique=True)
    password = models.CharField(max_length=255)


    def __str__(self):
        return f"{self.first_name} {self.last_name}"
    