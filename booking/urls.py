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
    # Profile & Editing
    path('profile/', views.users_profile, name='profile'),
    path('<int:pk>/add-info/', views.UserInfoUpdateView.as_view(), name='add_profile_info'),
    # Create slot / Confirmation / Delete
    path('create-slot/', views.CreateCoworkingSlotView.as_view(), name='create_slot'),
    path('<int:pk>/created-slot/', views.CreatedCoworkikngSlotOverView.as_view(), name='created_slot_overview'),
    path('<int:pk>/delete-slot/', views.DeleteCoworkingSlotView.as_view(), name='delete_slot'),
    # Slot List / Book Slot / Update / Delete
    path('slot-list/', views.CoworkingSlotListView.as_view(), name='slot_list_view'),
    path('<int:slot_id>/create-booking/', views.CreateBookingView.as_view(), name='create_booking'),
    path('<int:pk>/update-booking/', views.UpdateBookingView.as_view(), name='update_booking'),
    path('<int:pk>/delete-booking/', views.DeleteBookingView.as_view(), name='delete_booking'),
]


# BUG
# use slug fields and don't show actual primary key in url