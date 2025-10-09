from django.shortcuts import render

from cr.models import *


def login(request):
    return render(request,'user_profile/login.html')

def registration(request):

    universitys = University.objects.all()
    departments = Department.objects.all()

    context={
        'universitys':universitys,
        'departments':departments,
    }

    return render(request,'user_profile/registration.html',context)

def logout(request):
    pass

def user_dasboard(request):
    return render(request,'user_profile/user_dashboard.html')

def admin_dashboard(request):
    return render(request,'user_profile/admin_dashboard.html')