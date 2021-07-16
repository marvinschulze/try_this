from django.shortcuts import render, redirect

# Create your views here.
from django.shortcuts import get_object_or_404, render, redirect
# Import authentication views & decorators
from django.contrib.auth import views as auth_views
# from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

from .forms import CustomUserCreationForm



class LoginView(auth_views.LoginView):
    template_name = 'login/login.html'

class LogoutView(auth_views.LogoutView):
    next_page = 'booking:home'



def register(request):
    # check if user is already logged in, if so: redirect
    if request.user.is_authenticated:
        return redirect('booking:profile')
    else:  
        template_name = 'login/register.html' 
        if request.method == 'POST':
            form = CustomUserCreationForm(request.POST)
            if form.is_valid():
                form.save()
                return redirect('login:login')
        else:
            form = CustomUserCreationForm()

        return render(request, template_name, {'form':form})



############# [BUG] #############
# Login view is accesible when being logged in
# username is case sensitive!!! A) after username input in login --> .lower() B) when registering check against all possible capitalized usernames, then keep casesensitivity