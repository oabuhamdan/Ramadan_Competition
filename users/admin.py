from .models import *
from django.contrib import admin
from .models import CustomUser

# Register your models here.
admin.site.register(CustomUser)
admin.site.register(Point)
admin.site.register(PointsType)
