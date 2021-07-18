from django.shortcuts import get_object_or_404, render, redirect, reverse

# # Import authentication views & decorators
# from django.contrib.auth import views as auth_views
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

from .models import Booking

from django.views.generic.edit import CreateView, UpdateView


from .models import Booking, UserInfo, CowoSlot
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
            slot = CowoSlot.objects.get(id=form.cleaned_data['date'].id)
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
    future_slots = CowoSlot.objects.all().filter(date__gte=datetime.date.today()).order_by('date')
    CowoSlot_booking_joined = []

    # loop over query set and reformat results while getting related booking data
    for slot in future_slots:
    
        # get & format related bookings and sotre in list
        bookings_list = []
        for b in slot.booking_set.all():
            bookings_list.append("{} ({} - {})".format(b.username, b.time_start.strftime("%H:%M"), b.time_end.strftime("%H:%M")))

        # extract info from CowoSlot and combine with related bookings; append to combined set
        CowoSlot_booking_joined.append(
            {slot: {'date': slot.date, 't_start':slot.time_start, 't_end':slot.time_end, 'seats': slot.av_seats, 'bookings': bookings_list}}
            )

    return render(request, template_name, context={'slots': CowoSlot_booking_joined})


def users_profile(request):
    # check if a user is logged in 
    if not request.user.is_authenticated:
        return redirect('login:login')
    else:  
        template_name = 'booking/user-profile.html'
        this_user = User.objects.get(username=request.user.username)
        
        # <<< Trying to get additional Info for the user, if submitted >>>
        description = None
        curr_projects = None
        profile_image = None
        # Try getting a user's info from the DB; if found: check for added info; else return None (set above)
        try:
            this_user_info = UserInfo.objects.get(user=this_user.id)
            if this_user_info.description:
                description = this_user_info.description
            if this_user_info.current_projects:
                curr_projects = this_user_info.current_projects
            if this_user_info.profile_image:
                profile_image = this_user_info.profile_image
        except Exception as err:
            print("\nFinding user (attributes) throw an exception: \n" + str(err))

        rel_user_info = UserInfo.objects.get(user=request.user)

        user_info = {
            'first_name': this_user.first_name, 'nickname': this_user.username,
            'description': description, 'projects': curr_projects, 'profile_image': profile_image,
            'id':rel_user_info.id
            }

        # <<< Get future booked spots for the user, if any >>>
        future_bookings = Booking.objects.filter(username=this_user).filter(host_slot__date__gte=datetime.date.today()).order_by('host_slot__date')
        # bookings_and_coworkers = []
        # for booking in future_bookings:
        #     bookings_and_coworkers
        #     other_cowos = Booking.objects.filter(host_slot=booking.host_slot)
        #     other_cowos_info = []
        #     for cowo in other_cowos:
        #         other_cowos_info.append(
        #             {'username': cowo.username, 'time_start': cowo.time_start, 'time_end': cowo.time_end}
        #         )
        #     bookings_and_coworkers.append(
        #         {booking:other_cowos_info}
        #     )

            

        return render(request, template_name, {'user_info': user_info, 'bookings':future_bookings})



# Using update view and creating an empty row on user creation
class UserInfoUpdateView(UpdateView):
   
    template_name = "booking/add_user_info.html"
    model = UserInfo
    fields = ['description', 'current_projects']

    def get_success_url(self):
        return reverse('booking:profile')



############# [BUG] #############
# Make update user info inaccessible