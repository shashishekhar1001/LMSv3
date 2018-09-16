from django.shortcuts import render
from django.contrib import messages
from django.http import HttpResponseRedirect, HttpResponse
from lms.models import ContactModel
from lms.forms import ContactForm

def home(request):
    if request.method == 'POST':
        form = ContactForm(request.POST or None)
        if form.is_valid():
            name = form.cleaned_data.get('name')
            email = form.cleaned_data.get('email')
            subject = form.cleaned_data.get('subject')
            message = form.cleaned_data.get('message')

            newContact = ContactModel.objects.create(
                name = name,
                email = email,
                subject = subject,
                message = message
            )
            messages.success(request, 'Your message was sent successfully!')
            return HttpResponseRedirect('/thankyou')
        else:
            messages.error(request, 'Please correct the error below!')
    else:
        form = ContactForm()
    return render(request, "home.html", {'form':form})


def thankyou(request):
    return render(request, "thankyou.html", {})
