"""
URL configuration for djangoproject project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.urls import path, include
from .views import *
from django.conf import settings 
from django.conf.urls.static import static

urlpatterns = [
    
    path('', homepage, name="movie_list"),
    path('my-bookings/', my_bookings_view, name='my_bookings'),
    path('logout/', logout_view, name='logout'),
    path('signup/', signup_view, name='signup'),
    path('login/', login_view, name='login'),
    path('movie/<int:movie_id>/', movie_detail, name='movie_detail'),
    path('booking/<int:showtime_id>/', booking_view, name='booking_view'),
    path('checkout/<int:booking_id>/', checkout_view, name='checkout'),
]
