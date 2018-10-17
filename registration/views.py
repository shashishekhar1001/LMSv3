from django.core import signing
from django.core.exceptions import ValidationError
from django.conf import settings
from django.contrib.auth import authenticate, login, logout
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
            send_mail('Click the link below to activate yor Account for ' + "localhost:8080", 
            "http://" + "localhost:8080" +'/authentication/activate_user/?ak=' + ak, 
            settings.EMAIL_HOST_USER,
            [u.email], 
            fail_silently=False)
            activation_link = "http://" + "localhost:8080" +'/authentication/activate_user/?ak=' + ak
            print(activation_link)
            print("\n"*20)
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



def activation_failed(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('/account_active')
    return render(request, "activation_failed.html", {})


def activation_complete(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('/account_active')
    return render(request, "activation_complete.html", {})


def account_active(request):
    return render(request, "account_active.html", {})


def activate_user(request):
    salt = settings.SECRET_KEY
    ak = request.GET.get('ak')
    # Change below line max_age according to your settings.py file
    decrypt = signing.loads(ak, salt)
    u = User.objects.get(email=decrypt)
    try:
        if u.is_active == False:    
            u.is_active = True
            u.save()
            return HttpResponseRedirect('/activation_complete/')
        else:
            return HttpResponseRedirect('/account_active/')
    except:
        return HttpResponseRedirect('/activation_failed/')


def logout_view(request):
    logout(request)
    return HttpResponseRedirect("/")


def my_login(request):
    try:
        next = request.GET.get('next')
        if next:
            print(next)
        else:
            print("no next") 
    except Exception as e:
        print(e)
    form = LoginForm(request.POST or None)
    context ={"form":form}
    if form.is_valid():
        email = form.cleaned_data.get('email')
        password = form.cleaned_data.get('password')
        try:
            user = User.objects.get(email=email) 
            username = user.username
            user = authenticate(username=username, password=password)
        except:
            raise forms.ValidationError('User not found')
        if user is not None:
            if user.is_active:
                login(request, user)
                try:
                    custom_user = Custom_User.objects.get(user = user)
                except:
                    return HttpResponseRedirect('/signup/')
                try:
                    if custom_user is not None:
                        if str(custom_user.primary_registration_type) == str("Trainer"):
                            if next:
                                return HttpResponseRedirect(next) 
                            return HttpResponseRedirect('/trainer_dashboard/')
                        if str(custom_user.primary_registration_type) == str("Learner"):
                            if next:
                                return HttpResponseRedirect(next)       
                            return HttpResponseRedirect('/learner_dashboard/')
                except Exception as e:
                    print(e)
            else:
                return HttpResponseRedirect('/activation_pending/')
            return HttpResponseRedirect('/')
        else:
            messages.error(request, 'Incorrect Password.')
            context ={"form":form}      
    return render(request, "login.html", context)
