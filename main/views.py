from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from django.views import View
from .models import *
import datetime
import calendar
from django.contrib import messages
from .filter import deco_login

from .default_add import *


def add_day(request):
    default_add_day()
    return {"day":'added'}


def add_month(request):
    default_add_month()
    return {"month":'added'}



class HomeView(View):
    @deco_login
    def get(self,request):
        print()
        clients = Client.objects.all()
        all_clients = clients.count()
        payment = Payment.objects.all().order_by("-id")
        
        inactive = 0
        active = 0
        paused = 0
        for c in clients:
            if c.status == "ACTIVE":
                active += 1
            elif c.status == "INACTIVE":          
                inactive += 1
            else:
                paused += 1
        
        context = {
            "all_clients":all_clients,
            "active":active,
            "inactive":inactive,
            "paused":paused,
            "payment":payment

        }
        
        return render (request,'index.html',context)


class RegisterView(View):
    @deco_login
    def get(self,request):
        tarif =  ComingType.objects.all()

        context = {'tarif':tarif}
        return render(request,'register.html',context)

    def post(self,request):
        user = request.user
        name = request.POST.get('name')
        phone = request.POST.get('phone')
        ctypes = request.POST.get('tarif')
        if user and name and phone and ctypes:
            ctype = ComingType.objects.get(title=ctypes)
            status = request.POST.get('status')
            for c in Client.objects.all():
                if phone == c.phone:
                    messages.error(request, "Xatolik !!! Bu telefon raqam oldin ro'yxatdan o'tgan.")
                    return redirect('/register')
                else:
                    pass
            client = Client.objects.create(
                        user=user,
                        name=name,
                        phone=phone,
                        coming_type=ctype,
                        status=status,
                    )

            # month create

            now = datetime.datetime.now()
            today = int(now.strftime("%d"))
            month_days = calendar.monthrange(int(now.strftime("%Y")), int(now.strftime("%m")))[1]
            res_days = month_days - today
            if res_days >= client.coming_type.days:
                coming_days = client.coming_type.days
                price = client.coming_type.price
            else:
                daily_price = client.coming_type.price / client.coming_type.days
                coming_days = res_days
                price = daily_price * coming_days
            sunday = coming_days // 7
            coming_days -= sunday
            month = Month.objects.create(
                client=client,
                coming_days=coming_days,
                payment=int(price)
            )
            
            tarifs =  ComingType.objects.all()
            context = {'tarif':tarifs,'client':client, "uid":client.uid,"name":client.name}
            messages.success(request, "Mijoz ro'yxatga olindi !")
            return render(request=request, template_name='register.html',context=context)
        else:
            messages.success(request, "Xatolik qaytadan harakat qiling ! ")
            tarifs = ComingType.objects.all()
            context = {'tarif':tarifs, "status":"Nimadur noto`g`ri ketdi"} 
            return render(request,'register.html', context)




class DetailView(View):
    @deco_login

    def get(self, request, id):
        queryset = Client.objects.get(id=id)
        months = Month.objects.filter(client=queryset).order_by("-id")
        payment = months
        tarif = ComingType.objects.all()

        return render(request, "detail.html", {"client":queryset, "months":months, "tarifs":tarif})

    def post(self, request, id):
        if request.POST.get('delete'):
            client = Client.objects.filter(id=int(id))
            client.delete()
            messages.success(request, "Mijoz ro'yxatdan o'chirildi !")
            return redirect("main:list_client")
        else:

            name = request.POST['name']
            phone = request.POST['phone']
            status = request.POST['status']
            tarif = request.POST['tarif']
            tarif = ComingType.objects.get(title=tarif)
            client = Client.objects.filter(id=id)
            client.update(name=name, phone=phone, coming_type=tarif, status=status)
        return redirect(f"/detail/{id}")


def edit_day(request, day_id):
    day = get_object_or_404(Day, id=day_id)
    resp = request.GET.get('day_result')
    if resp == "true":
        day.came = True
        day.save()
        return JsonResponse({"came":"True"})
    elif resp == "false":
        day.came = False
        day.save()
        return JsonResponse({"came":"False"})
    else:
        return JsonResponse({"came":"not valid"})


def barcode_came(request, uid):
    try:
        client = get_object_or_404(Client, uid=uid)
        day = client.months.last().days.last()
        today = datetime.datetime.now().strftime('%Y-%m-%d')
        if str(today) == str(day):
            day.came = True
            day.save()
            status = f"{client.name} bugun mashg'ulotga keldi."
        else:
            status = f"{client.name} avval to'lovni amalga oshiring!"
    except:
        status = "UID noto`g`ri"
    return JsonResponse({"status":status})


class DavomatView(View):
    @deco_login

    def get(self,request):
        queryset = Client.objects.all().order_by("-id")
        tarif = ComingType.objects.all()
        data = {
            "clients":queryset,
            "tarif":tarif
        }
        return render (request,'new_table.html', data)


class PaymentView(View):
    @deco_login
    def get(self, request):
        try:
            client_id = request.GET['client_id']
            client = Client.objects.get(uid=client_id)
            month = Month.objects.filter(client=client).last()
            data = {
                "name":client.name,
                "uid":client.uid,
                "payment":month.payment,
                "balance":client.balance
            }
            return JsonResponse(data)
        except:
            clients = Client.objects.all()
            return render(request, 'forms-layouts.html', {"clients":clients})

    def post(self, request):
        clients = Client.objects.all()
        uid = request.POST.get('uid')
        payment = int(request.POST.get('payment'))
        discount = int(request.POST.get('discount'))
        balance = int(request.POST.get('balance'))
        discounted = payment + discount + balance
        try:
            obj = get_object_or_404(Client, uid=uid)
        except:
            obj = False
        if obj == False:
            return render(request, 'forms-layouts.html', {"response":"ID noto`g`ri berildi","status":"danger","clients":clients})
        else:
            month = Month.objects.filter(client=obj).last()
            if month.payment == discounted:
                month.payment = 0
                month.payed = True
                obj.debt = False
            elif month.payment < discounted:
                balance = discounted - month.payment
                month.payment = 0
                month.payed = True
                obj.debt = False
                obj.balance += balance
            else:
                month.payment -= discounted
                month.payed = False
                obj.debt = True
            month.save()
            # obj.balance -= balance
            obj.save()
            Payment.objects.create(
                month=month,
                money=payment,
                discount=discount
            )
            try:
                last_day = month.days.last().date
            except:
                last_day = 'no last day'
            today = datetime.datetime.now()
            if last_day != today:
                Day.objects.create(month=month)
            messages.success(request, "To'lov amalga oshirildi ! ")
            return redirect('/payment')


def detail_payment(request):
    month_id = int(request.POST.get('month_id'))
    payment = int(request.POST.get('payment'))
    month = Month.objects.get(id=month_id)
    obj = month.client
    if month.payment == payment:
        month.payment = 0
        month.payed = True
        obj.debt = False
    elif month.payment < payment:
        balance = payment - month.payment
        month.payment = 0
        month.payed = True
        obj.debt = False
        obj.balance = balance
    else:
        month.payment -= payment
        month.payed = False
        obj.debt = True
    month.save()
    obj.save()
    py = Payment.objects.create(
        month=month,
        money=payment
    )
    return JsonResponse({"status":"ok"})

def detail_month_sum(request):
    month_id = request.GET.get('id')
    month = Month.objects.get(id=month_id)
    payment = month.payment
    return JsonResponse({'payment':payment})

def handler_404(request,exception):
    return render(request, "404.html")

def handler_500(request):
    return render(request, "500.html")

