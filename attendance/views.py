from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from main.models import *
from .models import *
from django.views import View


def default_add_month(request, client_id):
    import datetime
    import calendar
    client = get_object_or_404(Client, id=client_id)
    now = datetime.datetime.now()
    today = int(now.strftime("%d"))
    month_days = calendar.monthrange(int(now.strftime("%Y")), int(now.strftime("%m")))[1]
    res_days = month_days - today
    if res_days >= client.coming_type.days:
        coming_days = client.coming_type.days
        price = client.coming_type.price
    else:
        daily_price = client.coming_type.price / client.coming_type.days
        print(daily_price)
        coming_days = res_days
        price = daily_price * coming_days
    sunday = coming_days // 7
    coming_days -= sunday
    month = Month.objects.create(
        client=client,
        coming_days=coming_days,
        payment=int(price)
    )
    return JsonResponse({"status":"Oy hosil qilindi"})


def default_add_day(request, client_id):
    client = get_object_or_404(Client, id=client_id)
    try:
        month = client.months.last()
        day = Day.objects.create(
            month=month
        )
    except:
        month = "salom"
    return JsonResponse({"status":"Kun hosil qilindi"})


class DavomatView(View):
    def get(self,request):
        queryset = Client.objects.all().order_by("-id")
        tarif = ComingType.objects.all()
        data = {
            "clients":queryset,
            "tarif":tarif
        }
        return render (request,'new_table.html', data)

    
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


