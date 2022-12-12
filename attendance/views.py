from django.shortcuts import render
from main.models import Client
# Create your views here.
from django.views import View



class DavomatView(View):
    def get(self,request):
        queryset = Client.objects.all().order_by("-id")
        data = {
            "clients":queryset
        }
        return render (request,'tables-general.html', data)



class StaticView(View):
    def get(self,request):
        return render (request,'static.html')