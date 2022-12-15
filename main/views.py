from django.shortcuts import render
from django.views import View
from .models import *
from attendance.models import *

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
        tarif =  ComingType.objects.all()


        # import calendar
        # import datetime
        # now = datetime.datetime.now()
        # year = now.strftime('%Y')
        # month = now.strftime('%m')
        # maxday = calendar.monthrange(int(year), int(month))
        # print(maxday[1])

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

        return render (request,'register.html',context)
