from django.shortcuts import redirect, render
from .models import *
# Create your views here.
def home(request):
    cr=CrProfile.objects.all().order_by('-created_at')
    total_university=University.objects.count()
    total_department=Department.objects.count()
    total_review=Review.objects.count()
    crs = sorted(
    CrProfile.objects.all(),
    key=lambda x: x.average_rating,
    reverse=True
    )

    context={
        'cr':cr,
        'total_university':total_university,
        'total_department':total_department,
        'total_review':total_review,
        'crs':crs,
        
    }
    return render(request,'home.html',context)

def all_cr(request):
    cr = CrProfile.objects.all()

    context={
        'cr':cr,
       
        
    }
    return render(request,'all_cr.html',context)

def latest_reviews(request):
    review=Review.objects.all().order_by('-created_at')[:10]

    context={
        'review':review,
    }
    return render(request,'latest_reviews.html',context)

def profile(request):
    return render(request,'profile.html')
def add_cr(request):
    return render(request,'add_cr.html')