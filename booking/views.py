from django.shortcuts import get_object_or_404, render, redirect

from .models import Booking, Timeslot
from .forms import BookingForm

import datetime

# Create your views here.

def home(request):
    template_name = 'booking/home.html'
    return render(request, template_name)

def booking(request):
    template_name = 'booking/booking.html'
    
    date_error = None

    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            # Validity check: available time selected?
            slot = Timeslot.objects.get(id=form.cleaned_data['date'].id)
            # get input for time_start & time_end
            t_s = form.cleaned_data['time_start']
            t_e = form.cleaned_data['time_end']
            # Compare for validity
            if t_s >= slot.time_start and t_s < slot.time_end and t_e <= slot.time_end and t_e > t_s:
                b = form.save() 
                return redirect("booking:booking-overview", b.id)
            else:
                form = BookingForm()
                date_error = 1
    else:
        form = BookingForm() 
    
    return render(request, template_name, {'form':form, 'date_error':date_error})

# Shows overview to user who just made a booking || BUG: accesible to anyone by url
def bookingOverview(request, booking_id):
    booking = get_object_or_404(Booking, pk=booking_id)
    template_name = 'booking/book-overview.html'
    return render(request, template_name, {'booking': booking})

def calendar(request):
    template_name = 'booking/calendar.html'

    # set up empty list for storing && acces database
    timeslot_booking_joined = []
    future_timeslots = Timeslot.objects.all().filter(date__gte=datetime.date.today()).order_by('date')

    # loop over query set and reformat results while getting related booking data
    for timeslot in future_timeslots:
    
        # get & format related bookings and sotre in list
        bookings_list = []
        for b in timeslot.booking_set.all():
            bookings_list.append("{} ({} - {})".format(b.name, b.time_start.strftime("%H:%M"), b.time_end.strftime("%H:%M")))

        # extract info from timeslot and combine with related bookings; append to combined set
        timeslot_booking_joined.append(
            {timeslot: {'date': timeslot.date, 't_start':timeslot.time_start, 't_end':timeslot.time_end, 'seats': timeslot.av_seats, 'bookings': bookings_list}}
            )

    return render(request, template_name, context={'slots': timeslot_booking_joined})




############# [BUG] #############
# bookingoverview accesible with url