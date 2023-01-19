from .models import *
from django.http import JsonResponse
import datetime as dt
import calendar
from django.shortcuts import redirect

NOW = dt.datetime.now()

def getyear_view(request):
    year = int(request.GET.get('year'))
    months = [1,2,3,4,5,6,7,8,9,10,11,12]
    months_name = []
    mount_year = []
    for m in months:
        months_obj = Month.objects.filter(created__year=year, created__month=m)
        mount_month = 0
        for i in months_obj:
            for p in i.payments.all():
                mount_month += p.money
        mount_year.append(mount_month)
        months_name.append(calendar.month_abbr[m])
    
    return JsonResponse({'mount':mount_year,'months':months_name})
    

def getclient_view(request):
    year = int(request.GET.get('year'))
    months = [1,2,3,4,5,6,7,8,9,10,11,12]
    count_year = []
    months_name = []
    for m in months:
        months_obj = Client.objects.filter(created__year=year, created__month=m)
        mount_month = 0
        for i in months_obj:
            mount_month += 1
        count_year.append(mount_month)
        months_name.append(calendar.month_abbr[m])
    
    return JsonResponse({'mount':count_year,'months':months_name})

def deco_login(fun):
    def wrapper(self,request,*args,**kwargs):
        if request.user.is_authenticated:
            return fun(self, request, *args, **kwargs)
        return redirect('main:login')
    return wrapper

