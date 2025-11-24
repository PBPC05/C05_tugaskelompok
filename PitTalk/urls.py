"""
URL configuration for C05 project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
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
from django.urls import path, include
from django.http import HttpResponse

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('main.urls')),
    path('forums/', include('apps.forums.urls')),
    path("information/", include(("apps.information.urls", "information"), namespace="information")),
    path('news/', include('apps.news.urls')),
    path('prediction/', include('apps.prediction.urls')),
    path('user/', include('apps.user.urls')),
    path('history/', include('apps.history.urls')),
    path('auth/', include('apps.authentication.urls')), 
]
