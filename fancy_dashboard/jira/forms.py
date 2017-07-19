from django.forms import ModelForm, PasswordInput

from .models import JiraClient


class JiraClientForm(ModelForm):
    class Meta:
        model = JiraClient
        fields = ['url', 'username', 'password', ]
        widgets = {
            'password': PasswordInput(),
        }
