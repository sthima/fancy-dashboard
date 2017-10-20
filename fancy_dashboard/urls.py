"""fancy_dashboard URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls.static import static
from django.conf.urls import url, include
from django.contrib import admin
from django.conf import settings
from rest_framework import routers

from .dashboard import urls as dashboard_urls
from .dashboard.views.sprints import SprintViewSet
from .views import RootView

router = routers.DefaultRouter()
router.register(r'sprint', SprintViewSet)

urlpatterns = [
    url(r'^v1/', include(router.urls)),
    url(r'^admin/', admin.site.urls),
    url(r'^dashboard/', include(dashboard_urls)),
    url(r'^$', RootView.as_view()),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
