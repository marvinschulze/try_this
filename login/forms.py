from django import forms 

# Built in Django Authentication
from django.contrib.auth.models import User
# from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError

class CustomUserCreationForm(forms.Form):
    username = forms.CharField()
    first_name = forms.CharField()
    last_name = forms.CharField()
    email = forms.EmailField()
    password1 = forms.CharField()
    password2 = forms.CharField()

    def clean_username(self):
        username = self.cleaned_data['username'].lower()
        r = User.objects.filter(username=username)
        if r.count():
            raise ValidationError("Username already exists.")
        return username   

    def clean_email(self):
        email = self.cleaned_data['email'].lower()
        r = User.objects.filter(email=email)
        if r.count():
            raise ValidationError("There is an account registered with this E-Mail.")
        return email   

    def clean_password2(self):
        p1 = self.cleaned_data['password1'].lower()
        p2 = self.cleaned_data['password2'].lower()
        if p1 and p2 and p1 != p2:
            raise ValidationError("Passwords don't match.")
        return p2

    def save(self, commit=True):
        user = User.objects.create_user(
            self.cleaned_data['username'],
            self.cleaned_data['email'],
            self.cleaned_data['password1']
        )
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.save()
        return user