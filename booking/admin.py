from django.contrib import admin

from booking.models import Booking, Timeslot, Coworker
# Register your models here.
admin.site.register(Booking)
admin.site.register(Timeslot)
admin.site.register(Coworker)