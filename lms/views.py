from django.shortcuts import render
from django.contrib import messages 
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.forms.models import model_to_dict
from registration.models import Custom_User, Trainer_Model
from lms.forms import UpdateTrainerProfileForm


@login_required(login_url='/login/', redirect_field_name='next')
def trainer_update_profile(request):
    user = request.user
    if user.is_active == False:
        return HttpResponseRedirect('/activation_pending/')
    cu = Custom_User.objects.get(user=user)
    if cu.primary_registration_type == "Trainer":
        trainer = Trainer_Model.objects.get(user=cu)
        print("\n"*20)
        print(trainer.describe_yourself)
        print(trainer.skills)
        if request.method == 'POST':
            city = request.POST.get('City')
            state = request.POST.get('State')
            country = request.POST.get('Country')
            describe_yourself = request.POST.get('Describe Yourself')
            skills = request.POST.get('Skills')
            linked_in_url = request.POST.get('Linkedin')
            print("\n"*20)
            print(city)
            print(state)
            print(country)
            print(describe_yourself)
            print(skills)
            print(linked_in_url)
            trainer.city = city
            trainer.state = state
            trainer.country = country
            trainer.describe_yourself = describe_yourself
            trainer.skills = skills
            trainer.linked_in_url = linked_in_url
            trainer.save()
        else:
            form = UpdateTrainerProfileForm(initial=model_to_dict(trainer))
    else:
        return HttpResponseRedirect("/not_a_trainer/")
    return render(request, "trainer_update_profile.html", {'trainer':trainer})


@login_required(login_url='/login/', redirect_field_name='next')
def trainer_dashboard(request):
    user = request.user
    if user.is_active == False:
        return HttpResponseRedirect('/activation_pending/')
    cu = Custom_User.objects.get(user=user)
    if cu.primary_registration_type == "Trainer":
        trainer = Trainer_Model.objects.get(user=cu)
        context = {}
        return render(request, "trainer_dashboard.html", context)
    else:
        return HttpResponseRedirect("/not_a_trainer/")



def dashboard_base(request):
    return render(request, "dashboard_base.html", {})



def not_a_trainer(request):
    return render(request, "not_a_trainer.html", {})
