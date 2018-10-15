from django.core import signing
from django.core.exceptions import ValidationError
from django.conf import settings
from django.contrib.auth.models import User
from django.contrib.sites.shortcuts import get_current_site
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render
from .forms import *
from .models import *

# Create your views here.


def custom_user_creation(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('/account_active')
    current_site = str(get_current_site(request))
    form = CommonRegistrationForm(request.POST or None)
    context = {"form": form}
    if form.is_valid():
        instance = form
        first_name = instance.cleaned_data.get("first_name")
        last_name = instance.cleaned_data.get("last_name")
        mobile = instance.cleaned_data.get("mobile")
        email = instance.cleaned_data.get("email")
        password = instance.cleaned_data.get("password")
        register_as = instance.cleaned_data.get("register_as")
        u, created = User.objects.get_or_create(email=email)
        if created == False:
            if u.is_active:
                return HttpResponseRedirect('/already_registered')
            else:
                return HttpResponseRedirect('/activation_pending')
        else:
            # Save User Model
            u.is_active = False
            u.is_staff = False
            u.is_superuser = False
            u.first_name = first_name
            u.last_name = last_name
            u.set_password(password)
            u.username = email
            u.save()
            # Save the Custom User Model
            custom_user = Custom_User.objects.create(user=u, mobile=mobile, primary_registration_type=register_as)
            custom_user.save()
            print(custom_user.primary_registration_type) 
            if str(custom_user.primary_registration_type) == "Trainer":
                new_trainer = Trainer_Model.objects.create(user=custom_user)
                new_trainer.save()
            if str(custom_user.primary_registration_type) == "Learner":
                new_leaner = Learner_Model.objects.create(user=custom_user)
                new_leaner.save()          
            # Encrypt Activation Link
            salt = settings.SECRET_KEY
            ak = signing.dumps(u.email, salt)
            # Send Activation Link to the newly registered user
            # send_mail('Click the link below to activate yor Account for ' + current_site, 
            # "http://" + current_site +'/authentication/activate_trainer/?ak=' + ak, 
            # settings.EMAIL_HOST_USER,
            # [u.email], 
            # fail_silently=False)
            # send_mail('Click the link below to activate yor Account for ' + "localhost:8080", 
            # "http://" + "localhost:8080" +'/authentication/activate_user/?ak=' + ak, 
            # settings.EMAIL_HOST_USER,
            # [u.email], 
            # fail_silently=False)
            return HttpResponseRedirect('/activation_mail_sent')
        context = {"form": form}
    return render(request, "signup.html", context)


def activation_mail_sent(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('/account_active')
    return render(request, "activation_mail_sent.html", {})


def already_registered(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('/account_active')
    return render(request, "already_registered.html", {})


def activation_pending(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('/account_active')
    return render(request, "activation_pending.html", {})


def account_active(request):
    return render(request, "account_active.html", {})