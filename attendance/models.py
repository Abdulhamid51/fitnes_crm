from django.db import models


class Month(models.Model):
    client = models.ForeignKey("main.Client", related_name="months", on_delete=models.CASCADE)
    # main coming_types dan olinadi
    coming_days = models.PositiveIntegerField("kelishi kerak bo`ldan kunlar")
    payment = models.PositiveIntegerField("to`lashi kerak bo`lgan summa")
    created = models.DateField(auto_now_add=True)
    
    came = models.PositiveIntegerField("kelgan kunlari", default=0)
    payed = models.BooleanField("To`landi", default=False)

    def __str__(self):
        return str(self.id)


class Day(models.Model):
    month = models.ForeignKey(Month, related_name="days", on_delete=models.CASCADE)
    date = models.DateField(auto_now_add=True)
    came = models.BooleanField(default=False)

    def __str__(self):
        return str(self.date)