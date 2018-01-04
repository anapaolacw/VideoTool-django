"""proyecto URL Configuration

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
from django.conf.urls import url
from django.contrib import admin
from apps.views import * 
from django.conf import settings
from django.conf.urls.static import static
from django.views.static import serve

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^home/', home),
    url(r'^quienes/', quienes),
    url(r'^iniciar/', iniciar),
    url(r'^busqueda/', busqueda),
    url(r'^registrar/', registrar),
    url (r'^masRecientes/', masRecientes),
    url (r'^masVistos/', masVistos),
    url (r'^masBuscados/', masBuscados),
    url(r'^accionIniciar/', accionIniciar),
    url(r'^accionRegistrar/', accionRegistrar),
    url(r'^vistaUsuario/', vistaUsuario),
    url (r'^contactar/', contactar),
    url (r'^verPerfil/', verPerfil),
    url (r'^subir/', subir),
    url (r'^videosSubidos/', videosSubidos),
    url (r'^verVideo/(?P<id_video>\d+)/$', verVideo),
    url (r'^verVideoMio/(?P<id_video>\d+)/$', verVideoMio),
    url (r'^ordenarRecientes/', ordenarRecientes),
    url (r'^ordenarVistos/', ordenarVistos),
    url (r'^ordenarBuscados/', ordenarBuscados),
    url (r'^importar/', importar),
    url (r'^buscar/', buscar),
    url (r'^cerrar/', cerrar),
]

if settings.DEBUG:
    urlpatterns += [
    url(r'^media/(?P<path>.*)$', serve, {
        'document_root': settings.MEDIA_ROOT,
        }),
    ]