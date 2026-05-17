from django.urls import path
from .views import provider_dashboard, accept_booking, reject_booking, complete_booking
from providers import views

urlpatterns = [
    path('dashboard/', provider_dashboard, name='provider_dashboard'),
    path('accept/<int:id>/', accept_booking, name='accept_booking'),
    path('reject/<int:id>/', reject_booking, name='reject_booking'),
    path('complete/<int:id>/', complete_booking, name='complete_booking'),
    path('become-provider/', views.become_provider, name='become_provider'),
]