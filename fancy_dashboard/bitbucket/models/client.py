from django.db import models


class BaseClient(models.Model):
    username = models.CharField(max_length=200)


class BitbucketClient(BaseClient):
    password = models.TextField()
    email = models.EmailField()

    # TODO encrypt using salt from settings
    def set_password(self, password):
        self.password = password

    # TODO decode using salt from settings
    def get_password(self):
        return self.password


class GithubClient(BaseClient):
    token = models.TextField()

    # TODO encrypt using salt from settings
    def set_token(self, token):
        self.token = token

    # TODO decode using salt from settings
    def get_token(self):
        return self.token
