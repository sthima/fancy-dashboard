from .base import *  # NOQA: F403

DEBUG = True
ALLOWED_HOSTS = ['*']

# We don't need a 1st tier authetntication for development
PASSWORD_HASHERS = (
    'django.contrib.auth.hashers.MD5PasswordHasher',
)
AUTH_PASSWORD_VALIDATORS = []

# Database settings
DATABASES['default']['NAME'] = 'postgres'  # NOQA: F405
DATABASES['default']['USER'] = 'postgres'  # NOQA: F405
DATABASES['default']['HOST'] = 'db'  # NOQA: F405
DATABASES['default']['PORT'] = '5432'  # NOQA: F405

# Email Config
# Must modify to production
SEND_DEBUG_EMAILS = False

if not SEND_DEBUG_EMAILS:
    EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
    EMAIL_FROM = "no-reply@sthima.com.br"
