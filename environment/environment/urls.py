"""
URL configuration for environment project.

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

from django.urls import path,include, re_path
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from frontend import views


urlpatterns = [
    re_path(r'^$', views.home, name='home'),
    re_path(r'^new_persona/$', views.new_persona, name='new_persona'),
    re_path(r'^move/$', views.move, name='move'),
    re_path(r'^update_persona/$', views.update_persona, name='update_persona'),
    re_path(r'^process_environment/$', views.process_environment, name='process_environment'),
    re_path(r'^update_environment/$', views.update_environment, name='update_environment'),
    
    path("admin/", admin.site.urls),
]
