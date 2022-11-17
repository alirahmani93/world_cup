from django.contrib import admin, messages
from django.contrib.auth.admin import UserAdmin as _UserAdmin

from common.admin import BaseAdmin
from user.models import User, Player, Feedback, PredictionArrange


# Admins
@admin.register(User)
class UserAdmin(_UserAdmin, BaseAdmin):
    list_display = ('username', 'mobile_number', 'email',)
    list_filter = ('is_active', 'is_staff', 'is_superuser',)
    search_fields = ('email', 'first_name', 'last_name', 'mobile_number', 'username',)
    readonly_fields = ('token',)

    def get_fieldsets(self, request, obj=None):
        fieldsets = super(UserAdmin, self).get_fieldsets(request, obj)
        try:
            if 'mobile_number' not in fieldsets[1][1]['fields']:
                fieldsets[1][1]['fields'] += ('mobile_number', 'token')
        except:
            pass
        return fieldsets


@admin.register(Player)
class PlayerAdmin(BaseAdmin):
    list_display = ('username', 'mobile_number', 'email',)
    list_filter = ('is_active', 'is_staff', 'is_superuser', 'is_blocked',)
    search_fields = ('mobile_number', 'username', 'profile_name', 'uuid', 'id', 'first_name', 'last_name',)
    readonly_fields = ('token', 'uuid', 'date_joined', 'last_login', 'updated_time')

    filter_horizontal = ('groups',)

    def save_model(self, request, obj, form, change):
        try:
            super(PlayerAdmin, self).save_model(request, obj, form, change)
        except Exception as e:
            self.message_user(request, e, messages.ERROR)


@admin.register(PredictionArrange)
class PredictionArrangeAdmin(BaseAdmin):
    list_display = ('player', 'match', 'winner', 'is_penalty',)
    list_filter = ('is_active', 'is_penalty', 'winner', 'is_processed', 'match')
    search_fields = (
        'match__team_1__name','match__team_2__name',
        'player__username', 'player__mobile_number', 'player__profile_name', 'uuid', 'id',)
    readonly_fields = (
        'is_processed',
        'player'
    )

    def save_model(self, request, obj, form, change):
        try:
            super(PredictionArrangeAdmin, self).save_model(request, obj, form, change)
        except Exception as e:
            return self.message_user(request, e, messages.ERROR)


@admin.register(Feedback)
class FeedbackAdmin(BaseAdmin):
    list_display = ('player', 'short_description')
    search_fields = ('player__username', 'player__mobile_number', 'player__profile_name',)
    readonly_fields = ('player',)
    list_filter = ('created_time', 'is_resolved')
