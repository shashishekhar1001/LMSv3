from django.contrib import admin

# Register your models here.
from .models import *

admin.site.register(Custom_User)
admin.site.register(Trainer_Model)