from django.shortcuts import render
from django.views import View
from .models import *


class HomeView(View):
    def get(self,request):
        clients = Client.objects.all()
        all_clients = clients.count()
        # active = Client.objects.filter(status="ACTIVE").count()   ## variant 1.
        # inactive = Client.objects.filter(status="INACTIVE").count()
        # paused = Client.objects.filter(status="PAUSED").count()

        inactive = 0
        active = 0
        paused = 0
        for c in clients:
            if c.status == "ACTIVE":
                active += 1
            elif c.status == "INACTIVE":          ## variant 2..
                inactive += 1
            else:
                paused += 1
        
        context = {
            "all_clients":all_clients,
            "active":active,
            "inactive":inactive,
            "paused":paused
        }
        return render (request,'index.html',context)
    

class RegisterView(View):
    def get(self,request):
        return render (request,'register.html')