from django.contrib import admin
from .models import Drone, DroneLog


class DroneAdmin(admin.ModelAdmin):
    list_display = ('serial', 'height', 'is_online', 'last_seen')
    readonly_fields = ('is_online',)


admin.site.register(Drone, DroneAdmin)


class DroneLogAdmin(admin.ModelAdmin):
    list_display = ('id', 'drone', 'timestamp')
    ordering = ['-timestamp']


admin.site.register(DroneLog, DroneLogAdmin)
