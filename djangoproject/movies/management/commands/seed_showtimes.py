import random
from datetime import date, time, timedelta
from django.core.management.base import BaseCommand
from django.utils import timezone
from django.db import IntegrityError
from movies.models import Movie, Screen, Showtime

class Command(BaseCommand):
    help = 'Automatically creates random showtimes for all movies and screens starting in the year 2039.'

    def add_arguments(self, parser):
        parser.add_argument('--days', type=int, help='Number of days to generate showtimes for', default=7)
        parser.add_argument('--shows_per_day', type=int, help='Approximate number of shows to create per day', default=20)

    def handle(self, *args, **options):
        days = options['days']
        shows_per_day = options['shows_per_day']
        
        movies = list(Movie.objects.all())
        screens = list(Screen.objects.all())
        
        if not movies or not screens:
            self.stdout.write(self.style.ERROR('Please add at least one movie and one screen first.'))
            return

        # --- THIS IS THE KEY CHANGE ---
        # We now start from a fixed future date instead of today.
        start_date = date(2039, 1, 1)
        # --- END OF CHANGE ---

        created_count = 0

        for i in range(days):
            current_date = start_date + timedelta(days=i)
            for _ in range(shows_per_day):
                random_movie = random.choice(movies)
                random_screen = random.choice(screens)
                random_hour = random.randint(10, 22)
                random_minute = random.choice([0, 15, 30, 45])
                random_price = random.choice([250, 300, 350, 400, 450])
                
                show_time = time(hour=random_hour, minute=random_minute)
                
                naive_datetime = timezone.datetime.combine(current_date, show_time)
                aware_datetime = timezone.make_aware(naive_datetime, timezone.get_current_timezone())

                try:
                    Showtime.objects.create(
                        movie=random_movie,
                        screen=random_screen,
                        start_time=aware_datetime,
                        price=random_price
                    )
                    created_count += 1
                except IntegrityError:
                    pass
        
        self.stdout.write(self.style.SUCCESS(f'Successfully created {created_count} new showtimes starting from {start_date}.'))