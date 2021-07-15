from django import forms 

from .models import Booking
from django.contrib.auth.models import User


class BookingForm(forms.ModelForm):
    # specify model to use
    class Meta:
        model = Booking
        
        fields = "__all__"

class RegisterForm(forms.ModelForm):

    class Meta:
        model = User
        fields = "username", "password"
