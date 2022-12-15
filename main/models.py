from django.db import models
from django.contrib.auth.models import User

class Client(models.Model):
    user = models.ForeignKey(User, related_name="clients", on_delete=models.CASCADE)

    name = models.CharField("Ism familiyasi", max_length=150)
    phone = models.CharField("Telefon raqami", max_length=50)
    coming_type = models.ForeignKey("main.ComingType", related_name="type_clients",
                                    on_delete=models.SET_NULL, blank=True, null=True)
    STATUS_TYPES = (
        ("ACTIVE","active"),
        ("INACTIVE","inactive"),
        ("PAUSED","paused")
    )
    status = models.CharField(choices=STATUS_TYPES, max_length=50, blank=True, null=True)
    debt = models.BooleanField("Qarzi bor", default=True)
    created = models.DateField("Qo'shilgan sana", auto_now_add=True)
    updated = models.DateTimeField("O'zgartirilgan vaqt", auto_now=True)

    def __str__(self):
        return self.name


class ComingType(models.Model):
    title = models.CharField("Tarif nomi", max_length=50)
    days = models.PositiveIntegerField("Kunlari(bir oyda nech kun)")
    price = models.PositiveIntegerField("Narxi")
    info = models.TextField("Tarif xaqida ma'lumot", blank=True)

    def __str__(self):
        return self.title