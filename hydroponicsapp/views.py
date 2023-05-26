import re
from django.shortcuts import render, redirect
from django.utils.timezone import datetime
from django.http import HttpResponse, HttpResponseRedirect

from .models import *
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from .forms import *
import json

def home(request):
    return render(request,"Login.html")

def control_panel(request):
    
    pending = Notifications.objects.all()
    return render(request, "Control Panel.html", {'pending':pending})

def notification(request):
    context = {
        'notif' : Notifications.objects.all(),
        'total' : Notifications.objects.all(),
        'pending' : Notifications.objects.all()
    }
    return render(request, "Notifications.html",context)

#

def delete(request, notification_id):
    notification = Notifications.objects.get(id = notification_id)
    notification.delete()
    return HttpResponseRedirect("Notifications.html")

def history(request):
    context = {
        'notif' : Notifications.objects.all(),
        'total' : Notifications.objects.all(),
        'pending' : Notifications.objects.all()
    }
    return render(request, "History.html",context)

def logout(request):
    return redirect("Login")

def login(request):
    form = UserLoginForm(request.POST or None)
    msg = None
    if request.method == 'POST':
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')

            user = authenticate(request, username=username, password=password)
        
            print (username, password)

            if user is not None:
                print("success")
                return redirect ('ControlPanel')
            else:
                msg='Invalid Credentials'
                return redirect ('Login') 
    return render (request, 'Login.html', {'form': form})

def Register(request):
    form = UserRegistration()
    if request.method == 'POST':
        form = UserRegistration(request.POST)
        if form.is_valid():
            form.save()
            return redirect ('Login')
        else:
            print(form)
            print("error")
    context = {'form':form}
    return render (request,'Registration.html', context)
