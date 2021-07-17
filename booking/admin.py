from django.contrib import admin

from booking.models import Booking, CowoSlot, UserInfo

# # That's how you add more preview in admin interface
class BookingAdmin(admin.ModelAdmin):
    list_display = ('username', 'host_slot', 'time_start', 'time_end')
class CowoSlotAdmin(admin.ModelAdmin):
    list_display = ('host_username', 'date', 'time_start', 'time_end', 'av_seats')
class UserInfoAdmin(admin.ModelAdmin):
    list_display= ('id', 'user')
    

# Register your models here.
admin.site.register(Booking, BookingAdmin)
# admin.site.register(Booking)
admin.site.register(CowoSlot, CowoSlotAdmin)
# admin.site.register(CowoSlot)
admin.site.register(UserInfo, UserInfoAdmin)