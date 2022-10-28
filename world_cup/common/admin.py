from django.contrib import admin
from .models import Configuration, CorrectPredictScore


class BaseAdmin(admin.ModelAdmin):
    save_on_top = True
    list_display = ['__str__', ]
    list_filter = []
    search_fields = []

    list_select_related = True
    list_per_page = 100
    list_max_show_all = 200

    save_as = True
    save_as_continue = True
    preserve_filters = True

    # Actions
    actions = []
    actions_on_top = True
    actions_on_bottom = True

    def get_list_display_links(self, request, list_display):
        return self.get_list_display(request)


class GeneralAdmin(BaseAdmin):
    save_on_top = True
    list_display = [
        "uuid",
        "is_active",

    ]
    list_filter = [
        "is_active",
    ]
    search_fields = [
        "id",
        "uuid",
    ]


class BaseInline(admin.StackedInline):
    """
    Defines SOME_ADMIN inline model.
    """
    model = None
    filter_horizontal = []
    extra = 0


@admin.register(Configuration)
class ConfigurationAdmin(BaseAdmin):
    list_display = (
        'app_name',
        'maintenance_mode',
        'app_version',
        'app_version_bundle',
        'last_bundle_version',
        'minimum_supported_bundle_version',
    )


@admin.register(CorrectPredictScore)
class CorrectPredictScoreAdmin(BaseAdmin):
    list_display = (
        'goal_score',
        'assist_goal_score',
        'yellow_card_score',
        'red_card_score',
        'arrange_score',
        'change_player_score',
    )
