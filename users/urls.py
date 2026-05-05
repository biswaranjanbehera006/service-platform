from django.urls import path
from .views import cancel_booking, logout_view, register_view, login_view, user_dashboard

urlpatterns = [
    path('register/', register_view, name='register'),
    path('login/', login_view, name='login'),
    path('dashboard/', user_dashboard, name='user_dashboard'),
    path('logout/', logout_view, name='logout'),
    path('cancel/<int:id>/', cancel_booking, name='cancel_booking'),
]