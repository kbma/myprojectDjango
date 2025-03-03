"""
URL configuration for myproject project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
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
from myapp.views import home
from myapp.views import commande,commande_confirmation
from myapp.views import generate_pdf


urlpatterns = [
    path('admin/', admin.site.urls),
    path('',home,name='home'),
    path('commande/<int:product_id>/', commande, name='commande'),
    path('commande-confirmation/<int:commande_id>/', commande_confirmation, name='commande_confirmation'),
    path('commande-confirmation-pdf/<int:commande_id>/', generate_pdf, name='generate_pdf'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
