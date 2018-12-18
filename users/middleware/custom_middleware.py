import allauth

from users.models import User
from allauth.socialaccount.models import SocialAccount
from allauth.account.signals import user_signed_up
from django.core.signals import request_finished
from django.core.signals import request_finished
from django.dispatch import receiver


class SimpleMiddleware:

    def __init__(self, get_response):
        self.get_response = get_response
        # One-time configuration and initialization.

    def __call__(self, request):
        # Code to be executed for each request before
        # the view (and later middleware) are called.

        response = self.get_response(request)
        a = SocialAccount.objects.all().first()
        # print(user_signed_up)
        # request_finished.connect(my_callback)
        # Code to be executed for each request/response after
        # the view is called.

        return response

#
# @receiver(request_finished)
# def my_callback(sender, **kwargs):
#     print("Request finished!")
