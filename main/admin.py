from django.contrib import admin
from .models import*

admin.site.register(Client)
admin.site.register(ComingType)
admin.site.register(Month)
admin.site.register(Day)
admin.site.register(Payment)
admin.site.register(Expense)
admin.site.register(ExpenseCategory)