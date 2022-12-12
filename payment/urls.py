from django.urls import path 
from .views import PaymentView,ListView


app_name = 'payment'

urlpatterns = [
    path('',PaymentView.as_view(),name='payment'),
    path('list',ListView.as_view(),name='list'),
]