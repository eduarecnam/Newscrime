from django.urls import path

from . import views

app_name = 'news'
urlpatterns = [
    path('', views.index, name='index'),
    path('forces', views.forces, name='forces'),
    path('details_force/<str:force>/', views.details_force, name='details_force'),
    path('seniors', views.seniors, name='seniors'),
    path('crimes', views.crimes, name='crimes'),   
]
