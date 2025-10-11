from django.shortcuts import render
from .models import *
# Create your views here.
def home(request):
    cr=CrProfile.objects.all().order_by('-created_at')
    total_university=University.objects.count()
    total_department=Department.objects.count()
    total_review=Review.objects.count()
   

    context={
        'cr':cr,
        'total_university':total_university,
        'total_department':total_department,
        'total_review':total_review,
    }
    return render(request,'home.html',context)

def all_cr(request):
    cr=CrProfile.objects.all()

    context={
        'cr':cr
    }
    return render(request,'all_cr.html',context)

def latest_reviews(request):
    return render(request,'latest_reviews.html')

def profile(request):
    return render(request,'profile.html')
def add_cr(request):
    return render(request,'add_cr.html')