from django.urls import path
from . import views


urlpatterns = [
    path('', views.index, name="index"),
    path('classes/', views.ClassListView.as_view(), name="classes"),
]
