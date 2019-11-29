from django.urls import path
from . import views

urlpatterns = [
    path('upload', views.upload, name='upload'),
    path('verify', views.verify, name='verify'),
    path('', views.index, name='index'),
]
