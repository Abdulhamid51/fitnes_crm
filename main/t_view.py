from django.shortcuts import render,redirect
from django.views import View
from .models import *
from django.contrib.auth import  login ,logout
from django.contrib import messages
from django.http import JsonResponse
from django.shortcuts import redirect
from .filter import deco_login


class LoginView(View):   
    def get(self,request):
        if  request.user.is_authenticated == True:
            return redirect('main:home')
        return render (request,'pages-login.html')

    def post(self,request):
        if  request.user.is_authenticated == True:
            return redirect('main:home')

        username = request.POST.get('username')
        password = request.POST.get('password')
        if username and password:
            user =  User.objects.filter(username=username)[0]

            if user is not None:
                login(request,user)
                return redirect('main:home')
        return render(request, 'pages-login.html')

def logout_(request):
    logout(request)
    return redirect('main:login')


class TarifView(View):
    @deco_login
    def get(self,request):
        tarif = ComingType.objects.all()
        context = {'tarif':tarif}

        return render(request,'tarif/tarif.html',context)

class AddTarif(View):
    @deco_login
    def get(self,request):
        tarif = ComingType.objects.all()
        return render(request, 'tarif/comingtype.html', {"tarif":tarif})
    def post(self,request):
        try:
            name = request.POST.get('name')
            days = request.POST.get('days')
            price = request.POST.get('price')
            info = request.POST.get('info')
            tarif  =  ComingType.objects.create(title=name,days=days,price=price,info=info)
            name = None
            if name == None:
                messages.success(request, "Tarif muvaffaqiyatli qo'shildi ! ")
                return redirect('/tarif')

        except:
            # messages.success(request, "Tarif muvaffaqiyatli qo'shildi. ")
            return render(request, 'tarif/comingtype.html')
class TarifUpdateview(View):
    @deco_login
    def get(self,request,pk):
        tarif = ComingType.objects.get(id=int(pk))
        context = {'tarif':tarif}
        return render(request, 'tarif/updatetarif.html',context)


    def post(self,request,pk):
        tarif = ComingType.objects.filter(id=int(pk))[0]
        name = request.POST.get('name')
        days = request.POST.get('days')
        price = request.POST.get('price')
        info = request.POST.get('info')
        if name:
            tarif.title = name
        if days:
            tarif.days = days
        if price:
            tarif.price = price
        if info:
            tarif.info = info
        else:
            tarif.info = ""
        tarif.save()
        messages.success(request, "Tarif muvaffaqiyatli o'zgartirildi ! ")
        return redirect('main:tarif')


class TarifDeleteview(View):
    @deco_login
    def get(self,request,pk):

        tarif = ComingType.objects.filter(id=int(pk))[0]
        tarif.delete()
        
        return JsonResponse({"status":"ok"})

    def post(self,request,pk):

        tarif = ComingType.objects.filter(id=int(pk))[0]
        tarif.delete()
        return JsonResponse({"status":"ok"})



# Chiqimlar


class ExpenseView(View):
    @deco_login
    def get(self,request):
        expense_category = ExpenseCategory.objects.all()
        expense = Expense.objects.all().order_by('-id')
        context = {
            "expense_category":expense_category,
            'expense':expense
        }
        return render(request,'expense/main_expense.html',context)

    def post(self, request):
        expense = request.POST.get('expense')
        summa = request.POST.get('summa')
        info = request.POST.get('info')
        category = request.POST.get('add_expense')

        edit_expense = request.POST.get('edit_expense')

        if expense is not None:
            c = ExpenseCategory.objects.get(id=expense)
            Expense.objects.create(category=c, summa=summa, info=info)
            messages.success(request, "Chiqim muvaffaqiyatli qo'shildi ! ")

        if category is not None:
            ExpenseCategory.objects.create(title=category)
            messages.success(request, "Chiqim turi muvaffaqiyatli qo'shildi ! ")
            

        return redirect('/expense')


class ExpenseDelUp(View):
    @deco_login
    def get(self, request, pk):
        cmd = request.GET.get('cmd')
        if cmd == "category_all":
            c = ExpenseCategory.objects.get(id=int(pk))
            c.expense_category.all()
            for i in c.expense_category.all():
                i.delete()
            
            c.delete()
        if cmd == "category":
            c = ExpenseCategory.objects.get(id=int(pk))
            c.delete()
        if cmd == "expense":
            c = Expense.objects.get(id=int(pk))
            c.delete()

        return JsonResponse({"status":"ok"})
    
    def post(self, request,pk):
        title = request.POST.get('edit_expense')
        c = ExpenseCategory.objects.get(id=int(pk))
        c.title = title
        c.save()

        messages.success(request, "Chiqim turi muvaffaqiyatli o'zgartirildi ! ")
        return redirect('/expense')

