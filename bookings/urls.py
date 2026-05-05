from django.urls import path
from .views import create_booking, update_booking_status
from bookings import views

urlpatterns = [
    path('book/', create_booking, name='create_booking'),
    path('update/<int:booking_id>/<str:status>/', update_booking_status, name='update_booking_status'),
    path('rate/<int:id>/', views.rate_booking, name='rate_booking'),
]