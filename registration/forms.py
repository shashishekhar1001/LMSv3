from django import forms
from .validators import validate_email, existing_email_validator, invalid_email, image_file_validator

class CommonRegistrationForm(forms.Form):
    first_name = forms.CharField(label='First Name', required=True)
    last_name = forms.CharField(label='Last Name', required=True)
    mobile = forms.CharField(max_length=20)
    email = forms.EmailField(required=True, validators=[validate_email, existing_email_validator])  
    password = forms.CharField(widget=forms.PasswordInput, required=True)
    REGISTRATION_CHOICES = (
        ('Learner', 'Learner'),
        ('Trainer', 'Trainer'),
        # ('Vendor', 'Vendor'),
        # ('Client', 'Client'),
        # ('Job Seeker', 'Job Seeker'),
    )
    register_as = forms.ChoiceField(choices=REGISTRATION_CHOICES, widget=forms.Select, required=True, label='Register As')


class LoginForm(forms.Form):
    email = forms.EmailField(required=True, label="Email", validators=[invalid_email])  
    password = forms.CharField(widget=forms.PasswordInput, required=True)
