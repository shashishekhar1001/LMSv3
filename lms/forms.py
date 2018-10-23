from django import forms

class ContactForm(forms.Form):
    name = forms.CharField(label='Your Name', required=True)
    email = forms.EmailField(label='Your Email', required=True)
    subject = forms.CharField(label='Subject', required=True)
    message = forms.CharField(label='Message', required=True, widget=forms.Textarea)

class UpdateTrainerProfileForm(forms.Form):
    city = forms.CharField(max_length=30, required=True)
    state = forms.CharField(max_length=30, required=True)
    country = forms.CharField(max_length=30, required=True)
    profile_picture = forms.ImageField(required=False)
    describe_yourself = forms.CharField(required=True, widget=forms.Textarea)
    linked_in_url = forms.URLField(required=True)
    skills = forms.CharField(required=True, widget=forms.Textarea)
    cv = forms.FileField(required=False)

