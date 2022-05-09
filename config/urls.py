"""head_hunter URL Configuration

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
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include
from django.urls import path

from config.error_handlers import custom_handler400
from config.error_handlers import custom_handler403
from config.error_handlers import custom_handler404
from config.error_handlers import custom_handler500
from junior_hunter.views import MainPageView


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', MainPageView.as_view(), name='main'),
    path('', include('accounts.urls')),
    path('vacancies/', include('junior_hunter.urls.vacancies')),
    path('companies/', include('junior_hunter.urls.companies')),
    path('mycompany/', include('junior_hunter.urls.mycompany')),
]


# TODO разобрать как это работает
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)

handler400 = custom_handler400
handler403 = custom_handler403
handler404 = custom_handler404
handler500 = custom_handler500
