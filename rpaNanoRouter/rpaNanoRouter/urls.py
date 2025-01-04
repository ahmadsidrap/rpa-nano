"""rpaNanoRouter URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
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
from django.contrib import admin
from django.urls import include, path
from .views import (
    RpaUp,
    RpaDown,
    RpaContainer,
    RpaActive,
    RpaImage,
    RpaVolume,
    RpaCopy,
    RpaNlp,
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/rpa/up', RpaUp.as_view(), name='rpa.input'),
    path('api/rpa/down', RpaDown.as_view(), name='rpa.down'),
    path('api/rpa/container', RpaContainer.as_view(), name='rpa.container'),
    path('api/rpa/active', RpaActive.as_view(), name='rpa.active'),
    path('api/rpa/image', RpaImage.as_view(), name='rpa.image'),
    path('api/rpa/volume', RpaVolume.as_view(), name='rpa.volume'),
    path('api/rpa/copy', RpaCopy.as_view(), name='rpa.copy'),
    path('api/rpa/nlp', RpaNlp.as_view(), name='rpa.nlp'),
]
