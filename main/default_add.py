import datetime
import calendar
from .models import *

def default_add_month():
    clients = Client.objects.all()
    for client in clients:
        last_month = str(client.months.last().created).split('-')[1]
        this_month = datetime.datetime.now().strftime('%m')
        if last_month != this_month:
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
            month = Month.objects.create(
                client=client,
                coming_days=coming_days,
                payment=int(price)
            )

def default_add_day():
    clients = Client.objects.all()
    for client in clients:
        try:
            last_day = str(client.months.last().days.last().date).split('-')[2]
            this_day = datetime.datetime.now().strftime('%d')
            cd = client.months.last().coming_days
            cm = client.months.last().came
            if cm >= cd or last_day == this_day:
                pass
            else:
                if client.status == "PAUSED" and client.months.last().payed == True:
                    pass
                else:
                    month = client.months.last()
                    month.came += 1
                    month.save()
                    day = Day.objects.create(
                        month=month
                    )
        except:
            pass