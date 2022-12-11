from django.shortcuts import render

# Create your views here.
from django.views import View


class PaymentView(View):
    def get(self,request):
        return render (request,'forms-layouts.html')




class ListView(View):
    def get(self,request):
        return render (request,'list.html')