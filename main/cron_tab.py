from models import *
from django.http import JsonResponse
import datetime, calendar

def default_add_day():
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
    return True


def default_add_month():

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
    return True


if __name__ == "__main__":
    default_add_day()
    if datetime.datetime.now().strftime('%d') == 1:
        default_add_month()