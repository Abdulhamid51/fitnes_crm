from .models import *
from django.http import JsonResponse
import datetime as dt
import calendar

NOW = dt.datetime.now()

def get_by_year(object:object, start:int, end:int):
    start_date = dt.date(start, 1, 1)
    end_date = dt.date(end, 1, 1)
    filtered_object = object.objects.filter(created__gte=start_date).filter(created__lte=end_date)
    return filtered_object

def get_by_month(object:object, start:int, end:int):
    year = NOW.strftime('%Y')
    start_date = dt.date(year, start, 1)
    end_date = dt.date(year, end, 1)
    filtered_object = object.objects.filter(created__gte=start_date).filter(created__lte=end_date)
    return filtered_object


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
    