from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.conf import settings
import os



class Custom_User(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    mobile = models.CharField(max_length=20)
    REGISTRATION_CHOICES = (
        ('Learner', 'Learner'),
        ('Trainer', 'Trainer'),
        ('Vendor', 'Vendor'),
        ('Client', 'Client'),
        ('Job Seeker', 'Job Seeker'),
    )
    primary_registration_type = models.CharField(max_length=15, choices=REGISTRATION_CHOICES)    
    secondary_registration_type = models.CharField(max_length=15, choices=REGISTRATION_CHOICES, blank=True)    
    tertiary_registration_type = models.CharField(max_length=15, choices=REGISTRATION_CHOICES, blank=True)    
    quaternary_registration_type = models.CharField(max_length=15, choices=REGISTRATION_CHOICES, blank=True)   
    
    def __str__(self):
        return self.user.email



class Trainer_Model(models.Model):
    user = models.ForeignKey(Custom_User, on_delete=models.CASCADE)
    city = models.CharField(max_length=30)
    state = models.CharField(max_length=30)
    country = models.CharField(max_length=30)
    profile_picture = models.ImageField(upload_to='profile_pics/%Y/%m/%d/', blank=True)
    courses_tutoring = models.TextField()
    describe_yourself = models.TextField()
    linked_in_url = models.URLField()
    skills = models.TextField(blank=True)
    cv = models.FileField(upload_to='cvs/%Y/%m/%d/', blank=True)

    def __str__(self):
        return self.user.user.email




# class Learner_Model(models.Model):
#     user = models.ForeignKey(Custom_User, on_delete=models.CASCADE)
#     profile_picture = models.ImageField(upload_to='profile_pics/%Y/%m/%d/', blank=True, null=True)
#     courses_learning = models.TextField()
#     courses_subscribed = models.ManyToManyField(Course, blank=True, null=True)

#     def __str__(self):
#         return self.user.user.email
