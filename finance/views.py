from django.shortcuts import render, redirect
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from datetime import datetime


# Create your views here.


def register_view(request):
    print("register_view_Called")
    print(request.method)
    if request.method == "POST":
        print("POST method called")
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        username = request.POST.get("username")
        password = request.POST.get("password")
        print(first_name, last_name, username, password)
        try:
            user = User.objects.create(
                first_name=first_name,
                last_name=last_name,
                username=username,
                email = username,
                date_joined = datetime.now()
            )
            user.set_password(password)
            user.save()
            print("user saved successfully")
            messages.info(request, "Account created successfully")
            return redirect("/finance/register/")
        except Exception as e:
            print(e)
            messages.error(request, str(e))
            return redirect("/finance/register/")

    return render(request, "auth/register.html")


def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        if not User.objects.filter(username=username).exists():
            messages.error(request, str("Username not found"))
            return redirect("/finance/login/")
            
        user = authenticate(username=username, password=password)
        if not user:
            messages.error(request, str("Invalid Password"))
            return redirect("/finance/login/")
        else:
            login(request, user)
            return redirect("/finance/dashboard")
    return render(request, "auth/login.html")


def dashboard_view(request):
    return render(request, "dashboard/user_profile.html")
    pass


def logout_view(request):
    logout(request)
    return redirect("/finance/login/")
