"""SRC URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
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
from django.urls import path

from django.conf import settings
from django.conf.urls.static import static

# from . import views as SRC_views
from SRC import views as SRC_views
from registration import views as reg_views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path(r'', SRC_views.home, name='home'),
    path(r'thankyou/', SRC_views.thankyou, name='thankyou'),
    path(r'signup/', reg_views.custom_user_creation, name='custom_user_creation'),
    path(r'activation_mail_sent/', reg_views.activation_mail_sent, name='activation_mail_sent'),
    path(r'already_registered/', reg_views.already_registered, name='already_registered'),
    path(r'activation_pending/', reg_views.activation_pending, name='activation_pending'),
    path(r'account_active/', reg_views.account_active, name='account_active'),
    path(r'activation_failed/', reg_views.activation_failed, name='activation_failed'),
    path(r'activation_complete/', reg_views.activation_complete, name='activation_complete'),
    path(r'activate_user/', reg_views.activate_user, name='activate_user'),
    path(r'logout/', reg_views.logout_view, name='logout'),
    path(r'login/', reg_views.my_login, name='login'),
    path(r'password_reset/', auth_views.password_reset, name='password_reset'),
    path(r'password_reset/done/', auth_views.password_reset_done, name='password_reset_done'),
    path(r'reset/done/', auth_views.password_reset_complete, name='password_reset_complete'),
    path(r'^reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$', auth_views.password_reset_confirm, name='password_reset_confirm')
]

if settings.DEBUG:
	urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
	urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
