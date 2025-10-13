from django.shortcuts import get_object_or_404, redirect, render
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
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
    crs = CrProfile.objects.all().order_by('-created_at')
    paginator = Paginator(crs, 12)
    page_number =  request.GET.get('page',1)

    try:
        crs = paginator.page(page_number)
    except PageNotAnInteger:
        crs = paginator.page(1)
    except EmptyPage:
        crs = paginator.page(1)

    context={
        'cr':crs,
        'paginator':paginator
       
        
    }
    return render(request,'all_cr.html',context)

def latest_reviews(request):
    reviews=Review.objects.all().order_by('-created_at')
    paginator = Paginator(reviews,10)
    page_number = request.GET.get('page',1)

    try:
        reviews = paginator.page(page_number)
    except PageNotAnInteger:
        reviews = paginator.page(1)
    except EmptyPage:
        reviews = paginator.page(1)

    context={
        'review':reviews,
        'paginator':paginator,
    }
    return render(request,'latest_reviews.html',context)

def cr_profile(request,slug):
  
    cr_profile=get_object_or_404(CrProfile,slug=slug)
    review=Review.objects.filter(cr_profile=cr_profile).order_by('-created_at')

    paginator = Paginator(review,5)
    page_number = request.GET.get('page',1)

    try:
        review=paginator.page(page_number)
    except PageNotAnInteger:
        review=paginator.page(1)
    except EmptyPage:
        review=paginator.page(1)

    context={
        'cr_profile':cr_profile,
        'review':review,
        'paginator':paginator,

    }
    
    return render(request,'profile.html',context)
def add_cr(request):
    return render(request,'add_cr.html')