from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from registration.models import Custom_User, Trainer_Model
from lms.forms import UpdateTrainerProfileForm

# Create your views here.
@login_required(login_url='/login/', redirect_field_name='next')
def trainer_update_profile(request):
    user = request.user
    if user.is_active == False:
        return HttpResponseRedirect('/activation_pending/')
    cu = Custom_User.objects.get(user=user)
    if cu.primary_registration_type == "Trainer":
        trainer = Trainer_Model.objects.get(user=cu)
        form = UpdateTrainerProfileForm(request.POST, request.FILES or None)
        context = {"form": form}
        if form.is_valid():
            instance = form
            city = instance.cleaned_data.get('city')
            state = instance.cleaned_data.get('state')
            country = instance.cleaned_data.get('country')
            profile_picture = instance.cleaned_data.get('profile_picture')
            describe_yourself = instance.cleaned_data.get('describe_yourself')
            linked_in_url = instance.cleaned_data.get('linked_in_url')
            skills = instance.cleaned_data.get('skills')
            cv = instance.cleaned_data.get('cv')

            trainer.city = city
            trainer.state = state
            trainer.country = country
            trainer.profile_picture = profile_picture
            trainer.describe_yourself = describe_yourself
            trainer.linked_in_url = linked_in_url
            trainer.skills = skills
            trainer.cv = cv
            trainer.save()
            return HttpResponseRedirect("/trainer_profile_updated/")            
        else:
            messages.error(request, 'Something went wrong.')
            form = UpdateTrainerProfileForm(request.POST, request.FILES or None)
            context = {"form": form}
    else:
        return HttpResponseRedirect("/not_a_trainer/")
    return render(request, "trainer_update_profile.html", context)


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