from django.contrib import admin

# Register your models here.
from admins.models import CompetitionArchive, UserArchive

admin.site.register(CompetitionArchive)
admin.site.register(UserArchive)
