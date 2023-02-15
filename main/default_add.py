import datetime
import calendar
from .models import *

def default_add_month():
    clients = Client.objects.all()
    for client in clients:
        last_month = str(client.months.last().created)
        this_month = datetime.datetime.now().strftime('%Y-%m-%d')
        if last_month != this_month:
            print(last_month)
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
        else:
            print('bu oy qoshilgan')