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
    earnings_year = [] 
    expense_year = []
    income_year = []
    for m in months:
        earnings = 0 # tushum
        expense = 0 # chiqim
        income_obj = Month.objects.filter(created__year=year, created__month=m)
        expense_obj = Expense.objects.filter(created__year=year,created__month=m)
        
        for i in income_obj:
            for p in i.payments.all():
                earnings += p.money
                
        for e in expense_obj:
            expense += e.summa

        earnings_year.append(earnings)
        expense_year.append(expense)
        income = earnings - expense
        income_year.append(income)
        months_name.append(calendar.month_abbr[m])
    
    return JsonResponse({
        'earnings':earnings_year,
        'expense':expense_year,
        'income':income_year,
        'months':months_name,
        })
    

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