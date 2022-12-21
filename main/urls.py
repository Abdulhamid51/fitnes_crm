from django.urls import path

from .views import HomeView , RegisterView, DetailView

app_name = 'main'

urlpatterns = [
    path('', HomeView.as_view(),name = 'home'),
    path('register/', RegisterView.as_view(),name = 'register'),
    path('detail/<int:id>', DetailView.as_view(),name = 'detail'),
]