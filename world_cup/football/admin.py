from django.contrib import admin
from .models import Team, TeamPlayer, Match, TeamPlayerAction

admin.site.register(Team)
admin.site.register(TeamPlayer)
admin.site.register(Match)
admin.site.register(TeamPlayerAction)
