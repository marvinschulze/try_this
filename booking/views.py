from django.shortcuts import get_object_or_404, render, redirect, reverse
from django.urls import reverse, reverse_lazy

# # Import authentication views & decorators
# from django.contrib.auth import views as auth_views
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User


from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.detail import DetailView, SingleObjectMixin
from django.views.generic.list import ListView

from django.core.exceptions import ValidationError
from django.contrib import messages


from .models import Booking, UserInfo, CowoSlot
from .forms import BookingForm, CreateSlotForm



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

# @login_required
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
        # <<< Get future booked spots for the user, if any >>>
        future_bookings = Booking.objects.filter(username=request.user).filter(host_slot__date__gte=datetime.date.today()).order_by('host_slot__date')
        # fetch all future slots where user is hosting, but not attending
        future_slots = CowoSlot.objects.filter(host_username=request.user).exclude(booking__username=request.user).filter(date__gte=datetime.date.today()).order_by('date')

        return render(request, template_name, {'bookings':future_bookings, 'slots':future_slots})



# Using update view and creating an empty row on user creation
class UserInfoUpdateView(UpdateView):
    template_name = "booking/add_user_info.html"
    model = UserInfo
    fields = ['description', 'current_projects']

    # def form_valid(self, form):
    #     form.instance.id = self.request.user.id
    #     return super().form_valid(form)

    def get_success_url(self):
        return reverse('booking:profile')

class CreateCoworkingSlotView(CreateView):
    template_name = "booking/create_slot.html"
    model = CowoSlot
    fields = ["date", "time_start", "time_end", "av_seats"]

    def form_valid(self, form):
        form.instance.host_username = self.request.user 
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('booking:created_slot_overview', kwargs={'pk': self.object.pk})

class CreatedCoworkikngSlotOverView(DetailView):
    template_name = "booking/created_slot_overview.html"
    model = CowoSlot

class DeleteCoworkingSlotView(DeleteView):
    template_name = "booking/delete_slot.html"
    model = CowoSlot

    def get_success_url(self):
        return reverse_lazy("booking:profile")

class UpdateBookingView(UpdateView):
    template_name = "booking/update_booking_view.html"
    model = Booking
    fields = ["time_start", "time_end"]
    time_error = "Enter a valid time which is in the slot's range."

    def slot(self):
        b = Booking.objects.get(pk=self.kwargs['pk'])
        slot = CowoSlot.objects.get(pk=b.host_slot.id)
        return slot


    def form_valid(self, form):
        # get logged in user, fetch Slot by slot_id (from url)
        form.instance.user = self.request.user
        slot = self.slot()
        form.instance.host_slot = slot

        # fetch the host slot and check if entered times are in range, if not call form_invalid
        t_s = form.cleaned_data['time_start']
        t_e = form.cleaned_data['time_end']
        
        # Compare for validity
        if t_s < slot.time_start or t_s > slot.time_end or t_e > slot.time_end or t_e < t_s:
            messages.error(self.request, self.time_error)
            return self.form_invalid(form)
        else:
            return super(UpdateBookingView, self).form_valid(form)


    def form_invalid(self, form):
        return super().form_invalid(form)

    def get_success_url(self):
        return reverse('booking:profile')

class DeleteBookingView(DeleteView):
    template_name = "booking/delete_booking.html"
    model = Booking

    def get_success_url(self):
        return reverse_lazy('booking:profile')


class CoworkingSlotListView(ListView):
    template_name = "booking/slot_list_view.html"
    # model = CowoSlot

    def get_queryset(self):
        queryset = CowoSlot.objects.filter(date__gte=datetime.date.today()).exclude(booking__username=self.request.user)
        return queryset


class CreateBookingView(CreateView):

    template_name = 'booking/create_booking.html'
    model = Booking
    fields = ["time_start", "time_end"]
    time_error = "Enter a valid time which is in the slot's range."
    dupli_error = "You are already booked in this slot!"


    def slot(self):
        slot = CowoSlot.objects.get(pk=self.kwargs['slot_id'])
        return slot


    def form_valid(self, form):
        # get logged in user, fetch Slot by slot_id (from url)
        form.instance.username = self.request.user
        pk = self.kwargs['slot_id']
        form.instance.host_slot = get_object_or_404(CowoSlot, pk=pk)

        # fetch the host slot and check if entered times are in range, if not call form_invalid
        slot = self.slot()
        t_s = form.cleaned_data['time_start']
        t_e = form.cleaned_data['time_end']
        
        # first check if there is a booking for this user with this slot
        # if Booking.objects.filter(host_slot=slot.id).filter(username=self.request.user).count():
        if Booking.objects.filter(host_slot=slot.id).filter(username=self.request.user).exists():
            messages.error(self.request, self.dupli_error)
            return self.form_invalid(form)
        # Compare for validity
        elif t_s < slot.time_start or t_s > slot.time_end or t_e > slot.time_end or t_e < t_s:
            messages.error(self.request, self.time_error)
            return self.form_invalid(form)
        else:
            return super(CreateBookingView, self).form_valid(form)


    def form_invalid(self, form):
        return super().form_invalid(form)

    def get_success_url(self):
        return reverse('booking:profile')







############# [BUG] #############
# Make update user info inaccessible to not logged in users (right now accesible via URL)