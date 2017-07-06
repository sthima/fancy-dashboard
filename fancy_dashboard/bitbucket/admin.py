from django.contrib import admin

from .models.client import BitbucketClient
from .forms.client import BitbucketClientForm


class BitbucketClientAdmin(admin.ModelAdmin):
    form = BitbucketClientForm


admin.site.register(BitbucketClient, BitbucketClientAdmin)
