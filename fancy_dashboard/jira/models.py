from django.db import models


class JiraClient(models.Model):
    username = models.CharField(max_length=200)
    password = models.TextField()
    url = models.URLField()

    # TODO encrypt using salt from settings
    def set_password(self, password):
        self.password = password

    # TODO decode using salt from settings
    def get_password(self):
        return self.password
