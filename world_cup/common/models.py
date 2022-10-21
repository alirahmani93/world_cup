from uuid import uuid4

from django.conf import settings
from django.core.cache import cache
from django.db import models
from django.utils.translation import gettext_lazy as _

from common.utils.time import standard_response_datetime, get_now
from common.utils.validators import version_regex


# Create your models here.


class BaseModel(models.Model):
    """All models in project inherit. These parameters are necessary. """
    uuid = models.UUIDField(verbose_name=_("UUID"), editable=False, default=uuid4)
    is_active = models.BooleanField(verbose_name=_("Is active"), default=True)
    updated_time = models.DateTimeField(verbose_name=_("Updated time"), auto_now=True)
    created_time = models.DateTimeField(verbose_name=_("Created time"), auto_now_add=True)

    def __str__(self):
        return f"{self.uuid}"

    class Meta:
        abstract = True


class SingletonBaseModel(BaseModel):
    """Used to ensure that a class can only have one concurrent instance."""

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        if not self.pk:
            if self.__class__.objects.count() == 1:
                raise Exception(_('Only one instance of configurations is allowed.'))
            self.created_time = get_now()
        super().save(*args, **kwargs)


class Configuration(SingletonBaseModel):
    """
        System configuration have some data are use in other entity and specifications.
    properties return static data at project
    """

    def get_app_name():
        return settings.PROJECT_NAME

    app_name = models.CharField(verbose_name=_("App Name"), max_length=255, default=get_app_name)
    deep_link_prefix = models.CharField(verbose_name=_("Deep link prefix"), max_length=255, blank=True, default='')
    maintenance_mode = models.BooleanField(verbose_name=_('Maintenance mode'), default=False)

    app_version = models.CharField(
        verbose_name=_("App Version"), max_length=100, default='1.0.0', validators=[version_regex])
    app_version_bundle = models.PositiveIntegerField(verbose_name=_("app version bundle"), default=1)
    last_bundle_version = models.PositiveIntegerField(verbose_name=_("Last bundle version"), default=1)
    minimum_supported_bundle_version = models.PositiveIntegerField(
        verbose_name=_("minimum supported bundle version"), default=1, )

    @property
    def server_time_zone(self):
        return settings.TIME_ZONE

    @property
    def server_time(self):
        return standard_response_datetime(get_now())

    @classmethod
    def load(cls):
        cache_data = cache.get(settings.CONFIGURATION_PREFIX)
        if cache_data:
            return cache_data
        data = cls.objects.get_or_create()[0]
        cache.set(settings.CONFIGURATION_PREFIX, data)
        return data

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        cache.set(settings.CONFIGURATION_PREFIX, self)
