from django.contrib import admin

from .models import UserData
from .models import OurUsers
from .models import Cities
#from .models import AuditEntry

admin.site.register(UserData)
admin.site.register(OurUsers)
admin.site.register(Cities)


""" @admin.register(AuditEntry)
class AuditEntryAdmin(admin.ModelAdmin):
    list_display = ['action', 'username', 'ip',]
    list_filter = ['action',] """