from django import forms

class ContactForm(forms.Form):
    name = forms.CharField(label='Your Name', required=True)
    email = forms.EmailField(label='Your Email', required=True)
    subject = forms.CharField(label='Subject', required=True)
    message = forms.CharField(label='Message', required=True, widget=forms.Textarea)