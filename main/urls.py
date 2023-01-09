from django.urls import path
from .views import *
from .t_view import *
from django.contrib.auth.decorators import login_required

app_name = 'main'

urlpatterns = [
    path('', HomeView.as_view(),name = 'home'),
    path('attandance/', DavomatView.as_view(), name='list_client'),
    path('register/', RegisterView.as_view(),name = 'register'),
    path('detail/<int:id>', DetailView.as_view(),name = 'detail'),
    path('add_default_day/<int:client_id>', default_add_day, name='add_day'),
    path('add_default_month/<int:client_id>', default_add_month, name='add_month'),
    path('add_day/<int:day_id>', add_day, name='add_day'),
    path('payment/', PaymentView.as_view(), name='payment'),

    path('tarif', TarifView.as_view(),name = 'tarif'),
    path('add/tarif', AddTarif.as_view(),name = 'addtarif'),
    path('update/tarif/<int:pk>',TarifUpdateview.as_view(),name='tarif_update'),
    path('delete/tarif/<int:pk>',TarifDeleteview.as_view(),name='tarif_delite'),
]