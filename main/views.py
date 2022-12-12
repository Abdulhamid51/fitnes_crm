from django.shortcuts import render
from django.views import View
from .models import *


class HomeView(View):
    def get(self,request):
        
        return render (request,'index.html')
    

class RegisterView(View):
    def get(self,request):
        return render (request,'register.html')