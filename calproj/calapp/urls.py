from django.urls import path
from .views import number_api

urlpatterns = [
    path('number/<str:qualification>/', number_api, name='number_api'),
]
