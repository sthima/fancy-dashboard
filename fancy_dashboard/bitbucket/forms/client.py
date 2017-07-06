from django.forms import ModelForm, PasswordInput

from ..models.client import BitbucketClient


class BitbucketClientForm(ModelForm):
    class Meta:
        model = BitbucketClient
        fields = ['username', 'password', 'email']
        widgets = {
            'password': PasswordInput(),
        }
