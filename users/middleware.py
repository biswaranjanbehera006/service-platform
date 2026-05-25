from django.conf import settings
from django.contrib import auth
from django.shortcuts import redirect
from django.contrib import messages
import time


class AutoLogoutMiddleware:

    def __init__(self, get_response):

        self.get_response = get_response


    def __call__(self, request):

        if request.user.is_authenticated:

            current_time = time.time()

            last_activity = request.session.get(
                'last_activity',
                current_time
            )

            # 5 MINUTES = 300 SECONDS
            if current_time - last_activity > 300:

                auth.logout(request)

                messages.warning(
                    request,
                    "⚠️ Session expired due to inactivity."
                )

                return redirect('login')

            request.session['last_activity'] = current_time

        response = self.get_response(request)

        return response