from django import forms 

from .models import Booking


class BookingForm(forms.ModelForm):
    # specify model to use
    class Meta:
        model = Booking
        
        fields = "__all__"




        
