from django.contrib import admin
from .models import *
# Register your models here.
admin.site.register(Movie)
admin.site.register(Theater)
admin.site.register(Screen)
admin.site.register(Showtime)
admin.site.register(Booking)
