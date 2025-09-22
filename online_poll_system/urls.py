"""
URL configuration for online_poll_system project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
"""from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView  # <-- import RedirectView
from rest_framework import routers
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.reverse import reverse

# DRF API root
@api_view(['GET'])
def api_root(request, format=None):
    return Response({
        'polls': reverse('poll-list', request=request, format=format),
        'options': reverse('option-list', request=request, format=format),
        'votes': reverse('vote-list', request=request, format=format),
    })

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('polls.urls')),
    path('api-root/', api_root, name='api-root'),  # browsable root
    path('', RedirectView.as_view(url='/api/', permanent=True)),  # redirect '/' to '/api/'
]
"""
# online_poll_system/urls.py
from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularSwaggerView,
    SpectacularRedocView,
)

urlpatterns = [
    path("admin/", admin.site.urls),

    # ✅ OpenAPI schema & docs
    path("api/schema/", SpectacularAPIView.as_view(), name="schema"),
    path("api/docs/", SpectacularSwaggerView.as_view(url_name="schema"), name="swagger-ui"),
    path("api/redoc/", SpectacularRedocView.as_view(url_name="schema"), name="redoc"),

    # ✅ Include app routes
    path("api/", include("polls.urls")),      # Polls endpoints
    path("api/auth/", include("auth_api.urls")),  # Auth endpoints (now isolated under /api/auth/)

    # ✅ Redirect root to API
    path("", RedirectView.as_view(url="/api/", permanent=True)),
]
