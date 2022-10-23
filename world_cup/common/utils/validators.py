from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator
from django.utils.translation import gettext_lazy as _

from common.utils.time import get_now


def validate_expire_date(value):
    if value < get_now():
        raise ValidationError("expire date must be later than now")
    return value


mobile_regex = RegexValidator(
    regex=r'^((?:0[0-9]{8,10})|(?:\+[0-9][0-9]{11,14}))$',
    message=_(
        "Phone number must be entered in the format:+989999999999' or '09999999999'.Up to 13 digits allowed.allowed characters: [0-9] and '+'."))

version_regex = RegexValidator(
    regex=r'^(\d+)\.(\d+)(?:\.(\d+))?(?:\-(\w+))?$',
    message=_("Phone number must be entered in the format: 111.222.333 "))
