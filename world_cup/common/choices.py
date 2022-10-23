from django.db import models
from django.utils.translation import gettext_lazy as _


class SMSModeKeys(models.TextChoices):
    SIGNIN = "in", _("sign in")
    SIGNUP = "up", _("sign up")
    RESEND = "re", _("resend")
