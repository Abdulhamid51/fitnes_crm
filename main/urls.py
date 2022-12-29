from django.urls import path
from .views import *
from django.contrib.auth.decorators import login_required

app_name = 'main'

urlpatterns = [
    path('', login_required(HomeView.as_view()),name = 'home'),
    path('attandance/', login_required(DavomatView.as_view()), name='list_client'),
    path('register/', login_required(RegisterView.as_view()),name = 'register'),
    path('detail/<int:id>', login_required(DetailView.as_view()),name = 'detail'),
    path('add_default_day/<int:client_id>', login_required(default_add_day), name='add_day'),
    path('add_default_month/<int:client_id>', login_required(default_add_month), name='add_month'),
    path('add_day/<int:day_id>', login_required(add_day), name='add_day'),
    path('payment/', login_required(PaymentView.as_view()), name='payment'),
]