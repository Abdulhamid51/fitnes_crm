from django.urls import path
from .views import *
from .t_view import *
from . import filter
from django.contrib.auth.decorators import login_required

app_name = 'main'

urlpatterns = [
    path('', HomeView.as_view(),name = 'home'),
    path('attandance/', DavomatView.as_view(), name='list_client'),
    path('register/', RegisterView.as_view(),name = 'register'),
    path('detail/<int:id>', DetailView.as_view(),name = 'detail'),
    path('add_default_day/', default_add_day, name='add_day'),
    path('add_default_month/', default_add_month, name='add_month'),
    path('add_day/<int:day_id>', edit_day, name='add_day'),
    path('payment/', PaymentView.as_view(), name='payment'),
    path('detail-payment/', detail_payment, name='detail-payment'),

    path('tarif', TarifView.as_view(),name = 'tarif'),
    path('add/tarif', AddTarif.as_view(),name = 'addtarif'),
    path('update/tarif/<int:pk>',TarifUpdateview.as_view(),name='tarif_update'),
    path('delete/tarif/<int:pk>',TarifDeleteview.as_view(),name='tarif_delite'),

    path('expense', ExpenseView.as_view(), name='expense'),
    path('expense/<int:pk>', ExpenseDelUp.as_view(), name='expense_del_up'),


    path("year_mount/", filter.getyear_view, name="year"),
    path("client_year_mount/", filter.getclient_view, name="client"),
]