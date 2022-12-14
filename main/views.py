from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from django.views import View
from .models import *

class HomeView(View):
    def get(self,request):
        
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
                                        status=status)
            tarif =  ComingType.objects.all()
            context = {'tarif':tarif,'client':client, "status":"Klient hosil qilindi"}
        else:
            context = {'tarif':tarif, "status":"Nimadur noto`g`ri ketdi"} 

        # month create
        import datetime
        import calendar

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

        return render(request, 'register.html', context)


class DetailView(View):
    def get(self, request, id):
        queryset = Client.objects.get(id=id)
        months = Month.objects.filter(client=queryset).order_by("-id")
        payment = months
        tarif = ComingType.objects.all()

        return render(request, "detail.html", {"client":queryset, "months":months, "tarifs":tarif})

    def post(self, request, id):
        name = request.POST['name']
        phone = request.POST['phone']
        status = request.POST['status']
        tarif = request.POST['tarif']

        tarif = ComingType.objects.get(title=tarif)
        client = Client.objects.filter(id=id)
    
        client.update(name=name, phone=phone, coming_type=tarif, status=status)

        return redirect(f"/detail/{id}")


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


class DavomatView(View):
    def get(self,request):
        queryset = Client.objects.all().order_by("-id")
        tarif = ComingType.objects.all()
        data = {
            "clients":queryset,
            "tarif":tarif
        }
        return render (request,'new_table.html', data)

    
    # def post(self, request):
    #     tarif = ComingType.objects.all()
    #     status = request.POST['status']
    #     coming_type = request.POST['tarif']
    #     debt = request.POST['debt']
    #     queryset = Client.objects.all()
    #     if status:
    #         queryset = queryset.filter(status=status)
    #     if coming_type:
    #         queryset = queryset.filter(coming_type=int(coming_type))
    #     if debt:
    #         queryset = queryset.filter(debt=bool(int(debt)))
    #     data = {
    #         "clients":queryset,
    #         "tarif":tarif
    #     }
    #     return render (request,'tables-general.html', data)



class PaymentView(View):
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
            Payment.objects.create(
                month=month,
                money=payment
            )
            Day.objects.create(month=month)
            return render(request, 'forms-layouts.html', {"response":"To'lov amalga oshirildi","status":"success","clients":clients})


