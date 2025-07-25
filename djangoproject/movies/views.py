from django.shortcuts import render, get_object_or_404
from .models import *
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.db.models.functions import Length
import razorpay
from collections import defaultdict

# Create your views here.

def signup_view(request):
    if request.method=='POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user= form.save()
            login(request, user)
            return redirect('movie_list')
        
    else:
        form= UserCreationForm()
        
    return render(request, 'signup.html', {'form': form})

def login_view(request):
    
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user() # Gets the authenticated user object
            login(request, user)   # Creates a session for the user
            return redirect('movie_list')
    
    else:
        form = AuthenticationForm() # Creates a blank form
    
    return render(request, 'login.html', {'form': form})

@login_required
def my_bookings_view(request):
    bookings = Booking.objects.filter(user=request.user).order_by('-booking_time')
    return render(request, 'my_bookings.html', {'bookings': bookings})


def homepage(request):
    
    selected_city = request.GET.get('city')
    search_query = request.GET.get('q') #Get the search query
    
    
    movies = Movie.objects.all()
    
    #applying city filer here if a city is selected
    if selected_city:
        movies = movies.filter(showtimes__screen__theater__city=selected_city). distinct()
        
    if search_query:
        movies = movies.filter(movie_name__icontains=search_query)
        
    cities = Theater.objects.values_list('city', flat=True).distinct()
    
    context ={'movies': movies, 'cities': cities, 'selected_city': selected_city, 'search_query': search_query, }
    return render(request, 'movie_list.html', context)


def logout_view(request):
    logout(request)
    return redirect('movie_list')

@login_required
def movie_detail(request, movie_id):
    movie = get_object_or_404(Movie, pk=movie_id)
    
      
        
    
    showtimes = Showtime.objects.filter(movie=movie, start_time__gte=timezone.now() #gte means greaterthanorequalto
    ).order_by('start_time')
    
    showtimes_by_date = defaultdict(list)
    for show in showtimes:
        show_date = show.start_time.date()
        showtimes_by_date[show_date].append(show)
    
    
    
    
    context={
        'movie': movie,
        'showtimes': showtimes
    }
    
    return render(request, 'movie_detail.html', context)



@login_required
def booking_view(request, showtime_id):
    showtime = get_object_or_404(Showtime, pk= showtime_id)
    all_seats = Seat.objects.filter(screen=showtime.screen).order_by(Length('seat_number'),'seat_number')
    
    
    booked_seat_ids = list(Booking.objects.filter(showtime=showtime).values_list('seats__id', flat=True))
    
    #for accepting data
    if request.method == 'POST':
        # 1. Get the list of selected seat IDs from the form
        selected_seat_ids = request.POST.getlist('seats')

        if not selected_seat_ids:
            # Handle case where no seats were selected
            return redirect('booking_view', showtime_id=showtime_id)

        # 2. Create the main Booking record
        booking = Booking.objects.create(
            user=request.user,
            showtime=showtime,
            total_price=len(selected_seat_ids) * showtime.price
        )

        # 3. THIS IS THE CRUCIAL STEP: Add the selected seats to the booking
        # The .add() method saves the relationship for a ManyToManyField.
        booking.seats.add(*selected_seat_ids)
        
        # 4. Redirect to a confirmation page
        return redirect('checkout', booking_id=booking.id)
    
            
    
    context={
        'all_seats': all_seats,
        'booked_seat_ids': booked_seat_ids,
    }
    
    return render (request, 'booking_page.html', context)


@login_required
def checkout_view(request, booking_id):
    # 1. Fetch the booking object
    booking = get_object_or_404(Booking, pk=booking_id, user=request.user)

    # 2. Create a Razorpay client
    client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))

    # 3. Create a Razorpay Order
    payment_data = {
        "amount": int(booking.total_price * 100), # Amount in paise
        "currency": "INR",
        "receipt": f"booking_{booking.id}",
    }
    razorpay_order = client.order.create(data=payment_data)
    
    context = {
        'booking': booking,
        'razorpay_order_id': razorpay_order['id'],
        'razorpay_key_id': settings.RAZORPAY_KEY_ID,
        'order_amount': payment_data['amount'],
    }

    return render(request, 'checkout.html', context)


    
    
    
    
    

        

