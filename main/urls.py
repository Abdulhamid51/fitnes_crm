from django.urls import path

from .views import HomeView , RegisterView

app_name = 'main'

urlpatterns = [
    path('', HomeView.as_view(),name = 'home'),
    path('register', RegisterView.as_view(),name = 'register'),
]