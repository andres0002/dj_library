"""
URL configuration for dj_library project.

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
# django
from django.contrib import admin
from django.conf import settings
from django.views.static import serve
from django.urls import path, include, re_path
# third
# own
from apps.base.views import Home
from apps.user.views import Login

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', Home.as_view(), name='index'),
    path('user/', include(('apps.user.urls', 'user'))),
    path('book/', include(('apps.book.urls', 'book'))),
    path('accounts/login/', Login.as_view(), name='login'),
]

#Media Files.
urlpatterns += [
    re_path(r'^media/(?P<path>.*)$', serve, {
        'document_root': settings.MEDIA_ROOT
    })
]