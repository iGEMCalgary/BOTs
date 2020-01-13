from django.urls import path
from sequence_optimization import views

urlpatterns = [path('', views.index, name='index'), ]
