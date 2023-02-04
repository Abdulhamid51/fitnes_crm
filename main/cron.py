from django_cron import CronJobBase, Schedule
from main.views import default_add_day
class MyCronJob(CronJobBase):
    print('working')
    RUN_EVERY_MINS = 0.5 # every 2 hours

    schedule = Schedule(run_every_mins=RUN_EVERY_MINS)
    code = 'main.views.default_add_day'    # a unique code

    def do(self):
        default_add_day()
        print('working do')
        pass    # do your thing here