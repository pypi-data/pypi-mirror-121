from django.urls import path

from .views import csv_view_export

urlpatterns = [
    path('<view>/', csv_view_export),
]
