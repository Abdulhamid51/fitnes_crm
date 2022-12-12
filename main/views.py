from django.shortcuts import render
from django.views import View
from .models import *
from attendance.models import MonthName

class HomeView(View):
    def get(self,request):

        return render (request,'index.html')


class RegisterView(View):
    def get(self,request):
        tarif =  ComingType.objects.all()

        context = {'tarif':tarif}
        return render (request,'register.html',context)

    def post(self,request):
        user = request.user
        name = request.POST.get('name')
        phone = request.POST.get('phone')
        tarif = request.POST.get('tarif')
        tarif = ComingType.objects.get(title=tarif)
        status = request.POST.get('status')

        client = Client.objects.create(user=user,
                                       name=name,
                                       phone=phone,
                                       coming_type=tarif,
                                       status=status)
        tarif =  ComingType.objects.all()
        if client:
            context = {'tarif':tarif,'client':client}
        else:
            context = {'tarif':tarif,}

        return render (request,'register.html',context)
