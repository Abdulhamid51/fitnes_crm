from django.db import models
from django.contrib.auth.models import  User
from django.db.models.signals import post_save
from django.dispatch import receiver


def random_numbers(lenth):
    import random
    RANDOM_NUMS = [0,1,2,3,4,5,6,7,8,9]
    rnums = ''
    for i in range(0, lenth):
        r = random.choice(RANDOM_NUMS)
        rnums += str(r)
    return rnums




class Client(models.Model):
    user = models.ForeignKey(User, related_name="clients", on_delete=models.CASCADE)
    uid = models.SlugField(blank=True,unique=True)
    name = models.CharField("Ism familiyasi", max_length=150)
    phone = models.CharField("Telefon raqami", max_length=50, unique=True)
    coming_type = models.ForeignKey("main.ComingType", related_name="type_clients",
                                    on_delete=models.SET_NULL, blank=True, null=True)
    STATUS_TYPES = (
        ("ACTIVE","Faol"),
        ("INACTIVE","Faolmas"),
        ("PAUSED","Pauza")
    )
    status = models.CharField(choices=STATUS_TYPES, max_length=50, blank=True, null=True)
    debt = models.BooleanField("Qarzi bor", default=True)
    created = models.DateField("Qo'shilgan sana", auto_now_add=True)
    updated = models.DateTimeField("O'zgartirilgan vaqt", auto_now=True)

    balance = models.IntegerField(default=0)

    def __str__(self):
        return self.name


class ComingType(models.Model):
    title = models.CharField("Tarif nomi", max_length=50)
    days = models.PositiveIntegerField("Kunlari(bir oyda nech kun)")
    price = models.PositiveIntegerField("Narxi")
    info = models.TextField("Tarif xaqida ma'lumot", blank=True)

    def __str__(self):
        return self.title

@receiver(post_save, sender=Client)
def uid_save(sender, instance, created, *args, **kargs):
    if created == True:
        try:
            uid = random_numbers(6)
            instance.uid = uid
        except:
            uid = random_numbers(6)
            instance.uid = uid
        instance.save()


class Month(models.Model):
    client = models.ForeignKey(Client, related_name="months", on_delete=models.SET_NULL, null=True, blank=True)
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


class Payment(models.Model):
    month = models.ForeignKey(Month, related_name="payments", on_delete=models.CASCADE)
    date = models.DateField(auto_now_add=True)
    money = models.IntegerField("Puli")
    discount = models.PositiveIntegerField("chegirma", default=0)

    def __str__(self):
        return str(self.date)


class ExpenseCategory(models.Model):
    title = models.CharField(max_length=255)
    created = models.DateField("Qo'shilgan sana", auto_now_add=True)

    def __str__(self):
        return str(self.title)


class Expense(models.Model):
    category = models.ForeignKey(ExpenseCategory, on_delete=models.SET_NULL , related_name='expense_category', null=True, blank=True)
    summa = models.IntegerField(default=0)
    info = models.TextField(blank=True, null=True)
    created = models.DateField("Qo'shilgan sana", auto_now_add=True)

    def __str__(self):
        return str(self.summa)


