from django.contrib import admin, messages
from django.utils.translation import gettext_lazy as _
from django_admin_listfilter_dropdown.filters import RelatedDropdownFilter, ChoiceDropdownFilter, SimpleDropdownFilter

from common.admin import GeneralAdmin, BaseInline
from common.utils.time import get_now
from .choices import MatchStatus
from .models import Team, TeamPlayer, Match, TeamPlayerAction, MatchResult


# Inlines
class TeamPlayerInline(BaseInline):
    model = TeamPlayer

    fieldsets = (
        (
            'General Info', {
                'fields': (
                    ('is_active', 'team', 'number'),
                )
            }
        ),
        (
            'Statistics info', {
                'fields': (
                    (
                        ('first_name', 'rank', 'last_name', 'is_banned_next_match',),

                    )
                ),
                'classes': ('extrapretty', 'wide', 'collapse', 'in'),
            }
        ),
    )


class TeamPlayerActionsInline(BaseInline):
    model = TeamPlayerAction
    fk_name = 'match'

    fieldsets = (
        (
            'General Info', {
                'fields': (
                    ('is_active', 'player', 'role'),
                )
            }
        ),
        (
            'Statistics info', {
                'fields': (
                    ('goal', 'assist_goal'),
                    ('is_change', 'is_best_player'),
                    ('yellow_card', 'red_card')
                ),
                'classes': ('extrapretty', 'wide', 'collapse', 'in'),
            }
        ),
    )


# Admins
@admin.register(Team)
class TeamAdmin(GeneralAdmin):
    radio_fields = {'continent': admin.HORIZONTAL, 'group': admin.HORIZONTAL, 'current_level': admin.HORIZONTAL}
    list_display = ['name', 'continent', 'group', 'current_level', ]
    list_filter = (
        ('continent', ChoiceDropdownFilter),
        ('group', ChoiceDropdownFilter),
        ('current_level', ChoiceDropdownFilter)
    )
    inlines = [TeamPlayerInline]


@admin.register(TeamPlayer)
class TeamPlayerAdmin(GeneralAdmin):
    list_display = ['first_name', 'last_name', 'number', 'team', 'is_banned_next_match', 'rank', ]
    list_filter = [('team', RelatedDropdownFilter), 'is_banned_next_match', 'rank', ]
    search_fields = ['first_name', 'last_name', 'number', 'team__name']
    search_help_text = 'first_name, last_name, number, team__name'


@admin.register(Match)
class MatchAdmin(GeneralAdmin):
    list_display = ['team_1', 'team_2', 'start_time', 'end_time',
                    'level', 'status',
                    'winner', 'is_penalty', ]
    list_filter = [('team_1', RelatedDropdownFilter), ('team_2', RelatedDropdownFilter),
                   ('level', ChoiceDropdownFilter), ('status', ChoiceDropdownFilter), 'winner',
                   'is_penalty', ]
    search_fields = ['team_1', 'team_2', 'level', 'status', 'winner', 'is_penalty', ]
    search_help_text = 'team_1, team_2, level, status, winner, is_penalty'

    actions = ['change_status_to_finish']
    inlines = [TeamPlayerActionsInline]

    def change_status_to_finish(self, request, queryset):
        """
        Defines a custom admin action that reverse the model is active value
        :return: a defined custom panel admin action
        """
        for q in queryset:
            if not q.winner:
                raise ValueError('winner status is empty.')
        queryset.update(end_time=get_now(), status=MatchStatus.FINISHED)

    change_status_to_finish.short_description = _('End Match')

    def save_model(self, request, obj, form, change):
        try:
            super(MatchAdmin, self).save_model(request, obj, form, change)
        except Exception as e:
            messages.set_level(request, messages.ERROR)
            messages.error(request=request, message=str(e))


@admin.register(MatchResult)
class MatchResultAdmin(GeneralAdmin):
    list_filter = ['winner', 'is_penalty','is_processed' ]
    list_display = ['match', 'winner', 'is_penalty', 'is_processed', 'best_player_id']
    search_fields = ['match']
    search_help_text = 'match'
    readonly_fields = ('is_processed',)
    actions = ['change_process']

    def change_process(self, request, queryset):
        """
        Defines a custom admin action that reverse the model is active value
        :return: a defined custom panel admin action
        """
        from .tasks import calculate

        for q in queryset:
            if not q.is_processed:
                calculate(match=q.match.id)
            else:
                messages.add_message(request, messages.WARNING, _(f'{q} is already processed'))

                # raise ValueError(f'{q} is already processed')

    change_process.short_description = _('Process results')
