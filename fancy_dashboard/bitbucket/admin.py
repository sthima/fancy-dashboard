from django.contrib import admin

from .models.client import BitbucketClient, GithubClient
from .forms.client import BitbucketClientForm


class BitbucketClientAdmin(admin.ModelAdmin):
    form = BitbucketClientForm


admin.site.register(BitbucketClient, BitbucketClientAdmin)
admin.site.register(GithubClient)
