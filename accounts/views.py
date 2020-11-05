from django.shortcuts import render
from django.utils.encoding import force_bytes, force_text
from django.contrib.sites.shortcuts import get_current_site
from main.models.accounts import User
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from django.http import HttpResponse, HttpResponseBadRequest
from main.utils.verification_token import TokenGenerator

# Create your views here.
def verify_email(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
        if user is not None and not user.email_verified and TokenGenerator().check_token(user, token=token):
            user.email_verified = True
            user.save()
            return HttpResponse("Done")
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        pass
    return HttpResponseBadRequest("Activation Link is Invalid!")
