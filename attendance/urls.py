from django.urls import path

from . views import DavomatView , StaticView, filter_client

app_name = 'attendance'

urlpatterns = [
    path ('',DavomatView.as_view(),name='list_client'),
    path ('static',StaticView.as_view(),name='static'),
    path ('filter/', filter_client, name='filter'),
]