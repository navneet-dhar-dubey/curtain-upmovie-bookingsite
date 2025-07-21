from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.conf import settings

# Create your models here.


class Movie(models.Model):
    movie_name= models.CharField(max_length=100)
    movie_description = models.TextField()
    duration_minutes = models.IntegerField(help_text="Duration in minutes")
    release_date = models.DateField()
    poster_image = models.ImageField(upload_to='movie_posters/', blank= True, null=True)
    language = models.CharField(max_length=50, default= "Hindi")
    rating =models.CharField(
        max_length=10,
        choices = [
            ('G', 'G - General Audiences'),
            ('PG', 'PG - Parental Guidance Suggested'),
            ('PG-13', 'PG-13 - Parents Strongly Cautioned'),
            ('R', 'R - Restricted'),
        ], blank=True, null=True
    )
    
    def __str__(self):
        return self.movie_name
    
    class Meta:
        ordering = ['release_date', 'movie_name']
        verbose_name = "Movie"
        verbose_name_plural = "Movies"
        
        
class Theater(models.Model):
    theater_name= models.CharField(max_length=150, unique=True)
    address = models.TextField()
    city = models.CharField(max_length=100)
    
    def __str__(self):
        return f"{self.theater_name} ({self.city})"

    class Meta:
        verbose_name = "Theater"
        verbose_name_plural = "Theaters"
        ordering = ['theater_name'] 
 
        
class Screen(models.Model):
    theater= models.ForeignKey('Theater',on_delete=models.CASCADE, related_name='screens')
    screen_name= models.CharField(max_length=100)
    screen_type = models.CharField(
        max_length=50,
        choices= [
            ('2D', '2D'),
            ('3D', '3D'),
            ('IMAX', 'IMAX'),
            ('ScreenX', 'ScreenX'),
            ('Other', 'Other')
        ],
        default='2D',
        blank=True,
        null=True
    )
    
    def __str__(self):
        return f"{self.theater.theater_name} - {self.screen_name}"
    
    class Meta:
        verbose_name = "Screen"
        verbose_name_plural = "Screens"
        unique_together = ('theater', 'screen_name')
        ordering = ['theater__theater_name', 'screen_name']
        

class Showtime(models.Model):
    movie = models.ForeignKey(Movie,  on_delete=models.CASCADE, related_name="showtimes")
    screen = models.ForeignKey(Screen, on_delete=models.CASCADE, related_name="showtimes")
    start_time = models.DateTimeField()
    price = models.IntegerField()
    
    def __str__(self):
        return f"{self.movie.movie_name} at {self.screen.screen_name}  - {self.screen.theater.theater_name} - {self.start_time.strftime('%Y-%m-%d %I:%M %p')}"        
    
    class Meta:
        verbose_name="Showtime"
        verbose_name_plural="Showtimes"
        unique_together= ('screen' , 'start_time') 
        ordering = ['start_time', 'screen__theater__theater_name', 'screen__screen_name']   
    


class Seat(models.Model):
    screen = models.ForeignKey(Screen, on_delete=models.CASCADE, related_name='seats')
    seat_number = models.CharField(max_length=10) # e.g., 'A1', 'B5'

    def __str__(self):
        return f"{self.screen} - Seat {self.seat_number}"
    
    class Meta:
        
        unique_together = ('screen', 'seat_number')
    
    
    
class Booking(models.Model):
    user =models.ForeignKey(User, on_delete=models.CASCADE, related_name="bookings")
    showtime = models.ForeignKey(Showtime, on_delete=models.CASCADE,related_name='bookings')
    seats = models.ManyToManyField(Seat)
    total_price =  models.IntegerField()
    booking_time = models.DateTimeField(auto_now_add=True)
    is_paid = models.BooleanField(default= False)
    
    def __str__(self):
        return (f"Booking by {self.user.username} for {self.seats} tickets "
                f"to {self.showtime.movie.movie_name} on "
                f"{self.showtime.start_time.strftime('%Y-%m-%d %I:%M %p')} "
                f"({'Paid' if self.is_paid else 'Unpaid'})")
    
    class Meta:
        verbose_name = "Booking"
        verbose_name_plural="Bookings"
        ordering= ['booking_time']
        
        

