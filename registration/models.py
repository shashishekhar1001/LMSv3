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
        # ('Vendor', 'Vendor'),
        # ('Client', 'Client'),
        # ('Job Seeker', 'Job Seeker'),
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
    profile_picture = models.ImageField(upload_to='profile_pics/%Y/%m/%d/', default="user.png")
    courses_tutoring = models.TextField()
    describe_yourself = models.TextField()
    linked_in_url = models.URLField()
    skills = models.TextField(blank=True)
    cv = models.FileField(upload_to='cvs/%Y/%m/%d/', blank=True)

    def __str__(self):
        return self.user.user.email


class Course(models.Model):
    thumbnail = models.ImageField(upload_to='Course_Thumbnails/%Y/%m/%d/', blank=True)
    course_by = models.ForeignKey(Trainer_Model, on_delete=models.CASCADE)
    course_name = models.CharField(max_length=200)
    description = models.TextField()
    prerequisite = models.TextField()
    requirements = models.TextField()
    rating = models.FloatField(default=0)
    no_of_ratings = models.FloatField(default=0)
    author = models.CharField(max_length=200, blank=True, default=None, null=True)
    fees = models.PositiveIntegerField(blank=True, default=0, null=True)

    def get_absolute_url(self):
        return reverse('edit_course', kwargs={'course_id': self.id})

    def save(self, *args, **kwargs):
        if getattr(self, 'author_changed', True):
            self.author = self.course_by.user.user.get_full_name()
        super(Course, self).save(*args, **kwargs)

    def __str__(self):
        return self.course_name + "  --By " + self.course_by.user.user.get_full_name()

    class Meta:
        permissions = (
            ('access_course', 'Access Course'),
        )


class Learner_Model(models.Model):
    user = models.ForeignKey(Custom_User, on_delete=models.CASCADE)
    profile_picture = models.ImageField(upload_to='profile_pics/%Y/%m/%d/', blank=True, null=True)
    courses_subscribed = models.ManyToManyField(Course, blank=True, null=True)
    cv = models.FileField(upload_to='cvs/%Y/%m/%d/', blank=True)

    def __str__(self):
        return self.user.user.email


