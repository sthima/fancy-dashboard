from django.contrib import admin

from .models import JiraClient
from .forms import JiraClientForm


class JiraClientAdmin(admin.ModelAdmin):
    form = JiraClientForm


admin.site.register(JiraClient, JiraClientAdmin)
