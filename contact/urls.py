from django.urls import path
from . import views


urlpatterns = [

    # =========================================
    # 📩 CONTACT PAGE
    # =========================================
    path(
        '',
        views.contact_page,
        name='contact'
    ),

]