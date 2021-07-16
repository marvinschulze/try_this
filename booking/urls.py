"""coworking URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path

from . import views

app_name = 'booking'

urlpatterns = [
    path('', views.home, name='home'),
    path('book-now/', views.booking, name='booking-index'),
    path('<int:booking_id>/book-overview/', views.bookingOverview, name='booking-overview'),
    path('calendar/', views.calendar, name="calendar"),
    path('profile/', views.users_profile, name='profile'),
]
