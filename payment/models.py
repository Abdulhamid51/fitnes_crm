from django.db import models

class Payment(models.Model):
    month = models.ForeignKey("appendance.Month", related_name="payments", on_delete=models.CASCADE)
    date = models.DateField(auto_now_add=True)
    money = models.IntegerField("Puli")

    def __str__(self):
        return str(self.date)