from django.contrib import admin

from user.models import User, Player, Feedback

# Register your models here.
admin.site.register(User)
admin.site.register(Player)
admin.site.register(Feedback)
