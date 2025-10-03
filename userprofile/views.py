from django.shortcuts import render


def login(request):
    return render(request,'user_profile/login.html')

def registration(request):
    return render(request,'user_profile/registration.html')

def logout(request):
    pass

def user_dasboard(request):
    return render(request,'user_profile/user_dashboard.html')

def admin_dashboard(request):
    return render(request,'user_profile/admin_dashboard.html')