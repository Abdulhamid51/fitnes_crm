from django.db import models


class MonthName(models.Model):
    name = models.CharField("Oy nomi", max_length=50)
    days = models.PositiveIntegerField("Oy kunlari")

    def __str__(self):
        return self.name


class Month(models.Model):
    client = models.ForeignKey("main.Client", related_name="months", on_delete=models.CASCADE)
    month_name = models.ForeignKey(MonthName, verbose_name="Oy", on_delete=models.CASCADE)
    # main coming_types dan olinadi
    coming_days = models.PositiveIntegerField("kelishi kerak bo`ldan kunlar")
    payment = models.PositiveIntegerField("to`lashi kerak bo`lgan summa")
    
    came = models.PositiveIntegerField("kelgan kunlari")
    payed = models.BooleanField("To`landi", default=False)

    def __str__(self):
        return self.month_name


class Day(models.Model):
    month = models.ForeignKey(Month, related_name="days", on_delete=models.CASCADE)
    date = models.DateField(auto_now_add=True)
    came = models.BooleanField(default=False)

    def __str__(self):
        return str(self.date)