from django.urls import path

from junior_hunter.views import CompanyView

urlpatterns = [
    path('<int:company_id>', CompanyView.as_view(), name='company'),

]
