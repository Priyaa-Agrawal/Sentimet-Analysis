from django.urls import path, include

from . import views

urlpatterns = [
    path('', views.index),
    path('textanalysis/', views.textanalysis),
    path('tweetanalysis/', views.tweetanalysis)
]
