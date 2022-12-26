from django.urls import path

from . views import *

app_name = 'attendance'

urlpatterns = [
    path ('',DavomatView.as_view(),name='list_client'),
    path ('static',StaticView.as_view(),name='static'),
    path ('add_default_day/<int:client_id>', default_add_day, name='add_day'),
    path ('add_default_month/<int:client_id>', default_add_month, name='add_month'),
    path ('add_day/<int:day_id>', add_day, name='add_day'),
]