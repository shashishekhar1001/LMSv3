from django.db import models

class ContactModel(models.Model):
    name = models.CharField(max_length=50)
    email = models.CharField(max_length=50)
    subject = models.CharField(max_length=300)
    message = models.CharField(max_length=500)

    def __str__(self):
        return self.name