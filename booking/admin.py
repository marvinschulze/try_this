from django.contrib import admin

from booking.models import Booking, Timeslot
# Register your models here.
admin.site.register(Booking)
admin.site.register(Timeslot)