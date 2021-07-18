from django import forms 

from .models import Booking, UserInfo


class BookingForm(forms.ModelForm):
    # specify model to use
    class Meta:
        model = Booking
        
        fields = "__all__"


# class UpdateUserInfoForm(forms.ModelForm):
#     class Meta:
#         model = UserInfo
#         fields = ["user", "description", "current_projects"]

        
