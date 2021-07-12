from django.shortcuts import get_object_or_404, render, redirect

from .models import Booking, Timeslot
from .forms import BookingForm

from datetime import date

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

    # context = {}
    # # fetch all dates in the database, that are today or in the future || collect bookings accordingly  
    # for timeslot in Timeslot.objects.all():
    #     print(timeslot)
    #     t = timeslot.values()
    #     print(t)

    # content = {}
    # future_timeslots = Timeslot.objects.all().select_related()
    # for slot in future_timeslots:
    #     slot_bookings = slot.booking_set.all()
    #     content[slot] = {'date': "now"}
    # print(content)

    # test = {"hello": "1221", "jlasd": 12213}
    future_timeslots = Timeslot.objects.filter(date__gte=date.today())
    print(future_timeslots.values())
    for f in future_timeslots:
        print(f.booking_set.all())
    # for f in future_timeslots:
    #     print(f.select_related())
    # apparently same effect:
    # future_timeslots = Timeslot.objects.all().filter(date__gte=date.today())

    test = {"first": {"date": 12}, "second": "you"}
    test2 = {"first": {"date": 12}, "second": "you"}

    return render(request, template_name, context={'test':test, 'test2': test2})




############# [BUG] #############
# bookingoverview accesible with url