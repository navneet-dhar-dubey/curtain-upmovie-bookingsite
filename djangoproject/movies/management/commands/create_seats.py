import string
from django.core.management.base import BaseCommand
from movies.models import Screen, Seat

class Command(BaseCommand):
    help = 'Creates seats for a given screen'

    def add_arguments(self, parser):
        parser.add_argument('--screen_id', type=int, help='The ID of the screen to add seats to')
        parser.add_argument('--rows', type=int, help='The number of rows of seats')
        parser.add_argument('--cols', type=int, help='The number of columns of seats')

    def handle(self, *args, **options):
        screen_id = options['screen_id']
        rows = options['rows']
        cols = options['cols']

        try:
            screen = Screen.objects.get(pk=screen_id)
        except Screen.DoesNotExist:
            self.stdout.write(self.style.ERROR(f'Screen with id "{screen_id}" does not exist.'))
            return

        # Clear existing seats for this screen to avoid duplicates
        Seat.objects.filter(screen=screen).delete()
        self.stdout.write(f'Cleared existing seats for screen {screen.screen_name}.')

        # Create new seats
        for i in range(rows):
            row_letter = string.ascii_uppercase[i]
            for j in range(1, cols + 1):
                seat_number = f"{row_letter}{j}"
                Seat.objects.create(screen=screen, seat_number=seat_number)
        
        self.stdout.write(self.style.SUCCESS(f'Successfully created {rows * cols} seats for screen "{screen.screen_name}".'))