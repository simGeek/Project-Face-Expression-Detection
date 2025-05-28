from django.urls import path
from home import views

urlpatterns = [
    path('', views.aqi_pollutants, name='aqi_pollutants'),
    path("aqi_regression/", views.aqi_regression, name='aqi_regression')
]
