"""twistedapp URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
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

from promomodels.views import qr_generator, redeem_code, test, optin, clear_db, report, home

urlpatterns = [
    path('admin/', admin.site.urls),
    path('qr_code/<str:code>/pic.png', qr_generator),
    path('redeem/in-store/<str:code>', redeem_code),
    path('send/<str:id>', test), 
    path('optin/<str:code>', optin),
    path('report/', report),
    path('', home),


    path('delete', clear_db)
]