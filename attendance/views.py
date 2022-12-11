from django.shortcuts import render

# Create your views here.
from django.views import View



class DavomatView(View):
    def get(self,request):
        return render (request,'tables-general.html')



class StaticView(View):
    def get(self,request):
        return render (request,'static.html')