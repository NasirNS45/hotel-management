from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView
from . import views

app_name = 'app'

urlpatterns = [
    path('', views.roombooking, name='roombooking'),
    path('contact/', views.contact, name='contact'),
    path('about/', views.about, name='about'),
    # path('register/', views.SignUpView.as_view(), name='register'),
    path('booking/', views.BookingView.as_view(), name='booking'),
    path('single/', views.single, name='single'),
    path('forgotpassword/', views.forgotpassword, name='forgot'),
    path('double/', views.double, name='double'),
    path('luxury/', views.luxury, name='luxury'),
    path('deluxe/', views.deluxe, name='deluxe'),
    path('executive/', views.executive, name='executive'),
    path('presidential/', views.presidential, name='presidential'),
    path('bookinghistory/', views.bookinghistory, name='history'),
    path('test/', views.test, name='test'),
    path('rooms/', views.rooms, name='rooms'),
    path('getusers/', views.getusers, name='getusers'),
    path('available_rooms/', views.available_rooms, name='available_rooms')
]
