from django import template

from django.conf import settings

register = template.Library()


@register.simple_tag()
def version():
    return settings.VERSION


@register.simple_tag()
def stage_url():
    return settings.STAGE_SERVER
