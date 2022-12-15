from django.shortcuts import render
from django.http import JsonResponse
from main.models import *
from django.views import View



class DavomatView(View):
    def get(self,request):
        queryset = Client.objects.all().order_by("-id")
        tarif = ComingType.objects.all()
        data = {
            "clients":queryset,
            "tarif":tarif
        }
        return render (request,'tables-general.html', data)
    
    def post(self, request):
        tarif = ComingType.objects.all()
        status = request.POST['status']
        coming_type = request.POST['tarif']
        debt = request.POST['debt']
        queryset = Client.objects.all()
        if status:
            queryset = queryset.filter(status=status)
        if coming_type:
            queryset = queryset.filter(coming_type=int(coming_type))
        if debt:
            queryset = queryset.filter(debt=bool(int(debt)))
        data = {
            "clients":queryset,
            "tarif":tarif
        }
        return render (request,'tables-general.html', data)


class StaticView(View):
    def get(self,request):
        return render (request,'static.html')


