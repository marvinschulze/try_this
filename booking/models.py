from django.db import models
import datetime

# Create your models here.

class Timeslot(models.Model):
    # table of available dates with available times 
    date = models.DateField()
    time_start = models.TimeField()
    time_end = models.TimeField()
    av_seats = models.CharField(max_length=2, default=5)

    def __str__(self):
        # convert date
        d = datetime.datetime.strptime(str(self.date), '%Y-%m-%d')
        date = str(d.strftime('%d.%m.%Y'))
        # convert time
        t_s = self.time_start.strftime("%H:%M")
        t_e = self.time_end.strftime("%H:%M")

        return("{} ({} - {} Uhr)").format(date, t_s, t_e)

    
class Booking(models.Model):
    # choices for connection:
    CONNECTION_CHOICES = [
        ('Friend', 'Friend'), 
        ('Wife', 'Wife'), 
        ('Roommate', 'Roommate'), 
        ('Family', 'Family'), 
        ('Stranger', 'Stranger')
    ]

    name = models.CharField(max_length=200)
    connection = models.CharField(
        max_length = 12, 
        choices = CONNECTION_CHOICES,
        default = 'Friend',
        )
    # Foreign Table Timeslot (table of date, time, and available seats for each open day)
    date = models.ForeignKey(Timeslot, default=1, verbose_name="timeslot", on_delete=models.CASCADE)
    # Check in the view that time_start and time_end are in the limit of Timeslots data // fetch object and return info with view
    time_start = models.TimeField()
    time_end = models.TimeField()

    def __str__(self):
        return ("[{}] - {} ({})").format(self.id, self.name, self.connection)




