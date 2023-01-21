from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from django.views import View
from .models import *
import datetime
import calendar
from django.contrib import messages
from .filter import deco_login


class HomeView(View):
    @deco_login
    def get(self,request):
        print()
        clients = Client.objects.all()
        all_clients = clients.count()
        

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
            "paused":paused
        }
        
        return render (request,'index.html',context)


class RegisterView(View):
    @deco_login

    def get(self,request):
        tarif =  ComingType.objects.all()

        context = {'tarif':tarif}
        return render (request,'register.html',context)

    def post(self,request):
        user = request.user
        name = request.POST.get('name')
        phone = request.POST.get('phone')
        tarif = request.POST.get('tarif')
        if user and name and phone and tarif:

            tarif = ComingType.objects.get(title=tarif)
            status = request.POST.get('status')

            client = Client.objects.create(user=user,
                                        name=name,
                                        phone=phone,
                                        coming_type=tarif,
                                        status=status,
                                        )
            tarif =  ComingType.objects.all()
            # context = {'tarif':tarif,'client':client, "status":"Klient hosil qilindi"}
            messages.success(request, "Mijoz muvaffaqiyatli ro'yxatga olindi ! ")

        else:
            messages.success(request, "Xatolik qaytadan harakat qiling ! ")
            # context = {'tarif':tarif, "status":"Nimadur noto`g`ri ketdi"} 

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

        return redirect('/register')


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

def default_add_month(request):

    clients = Client.objects.all()
    for client in clients:
        print('hhhhhhhhh')
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
    return JsonResponse({"status":"Oy hosil qilindi"})


def default_add_day(request):
    clients = Client.objects.all()
    for client in clients:
        try:
            if client.status == "PAUSED":
                pass
            else:
                month = client.months.last()
                month.came += 1
                month.save()
                day = Day.objects.create(
                    month=month
                )
        except:
            month = "salom"
    return JsonResponse({"status":"Kun hosil qilindi"})


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
        day.came = True
        day.save()
        status = "Mujos bugun mashg'ulotga keldi keldi"
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
            request.GET['client_id']
            client_id = int(request.GET['client_id'])
            client = Client.objects.get(uid=client_id)
            month = Month.objects.filter(client=client).last()
            data = {
                "name":client.name,
                "uid":client.uid,
                "payment":month.payment
            }
            return JsonResponse(data)
        except:
            clients = Client.objects.all()
            return render(request, 'forms-layouts.html', {"clients":clients})

    def post(self, request):
        clients = Client.objects.all()
        uid = request.POST.get('uid')
        payment = int(request.POST.get('payment'))
        try:
            obj = get_object_or_404(Client, uid=uid)
        except:
            obj = False
        if obj == False:
            return render(request, 'forms-layouts.html', {"response":"ID noto`g`ri berildi","status":"danger","clients":clients})
        else:
            month = Month.objects.filter(client=obj).last()
            if month.payment == payment:
                month.payment = 0
                month.payed = True
                obj.debt = False
            elif month.payment < payment:
                balance = payment - month.payment
                month.payment = 0
                month.payed = True
                obj.debt = False
                obj.balance += balance
            else:
                month.payment -= payment
                month.payed = False
                obj.debt = True
            month.save()
            obj.save()
            Payment.objects.create(
                month=month,
                money=payment
            )
            try:
                last_day = month.days.last().date
            except:
                last_day = 'no last day'
            today = datetime.datetime.now()
            if last_day == today:
                print("kun qoshilmadi")
            else:
                Day.objects.create(month=month)
                print("kun qoshildi")
            messages.success(request, "To'lov amalga oshirildi ! ")
            return redirect('/payment')


def detail_payment(request):
    month_id = int(request.POST.get('month_id'))
    payment = int(request.POST.get('payment'))
    month = Month.objects.get(id=month_id)
    obj = month.client
    if month.payment <= payment:
        month.payment = 0
        month.payed = True
        obj.debt = False
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



