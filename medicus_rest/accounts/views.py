from django.shortcuts import render
from django.views import View
from django.http import JsonResponse
from passlib.hash import django_pbkdf2_sha256 as handler
from .models import Account

class signup(View):
    def post(self, request):
        f_name = request.POST.get('firstName')
        l_name = request.POST.get('lastName')
        desig = request.POST.get('designation')
        email_id = request.POST.get('email')
        passwrd = handler.hash(request.POST.get('password'))
        Account.objects.create(first_name=f_name, last_name=l_name, designation=desig, email=email_id, password=passwrd)
        return JsonResponse({"message":"Successfull"})

class login(View):
    def post(self,request):
        email_id = request.POST.get('email')
        passwrd = request.POST.get('password')
        account_instance = Account.objects.get(email=email_id)
        if account_instance:
            if handler.verify(passwrd, account_instance.password):
                return JsonResponse({"message":"Successfull"})
            else:
                return JsonResponse({"message":"incorrect password"})
        else:
            return JsonResponse({"message":"account with email not present"})
