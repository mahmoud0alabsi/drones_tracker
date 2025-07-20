from django.contrib import admin
from .models import Drone, DroneLog


class DroneAdmin(admin.ModelAdmin):
    list_display = ('serial', 'height', 'is_online', 'last_seen')


admin.site.register(Drone, DroneAdmin)


class DroneLogAdmin(admin.ModelAdmin):
    list_display = ('drone', 'timestamp')


admin.site.register(DroneLog)
