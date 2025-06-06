from django.contrib import admin

# Register your models here.
from core.models import (
    Incident,
    Team,
    TeamMember, PoliceStation
)

admin.site.register(Incident)
admin.site.register(Team)
admin.site.register(TeamMember)
admin.site.register(PoliceStation)