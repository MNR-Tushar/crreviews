
from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .models import *
from userprofile.models import *
from django.contrib.auth.decorators import login_required
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


@login_required
def add_cr(request):

    university = University.objects.all()
    department = Department.objects.all()

    if request.method == 'POST':

       
        if hasattr(request.user, 'cr_profile'):
            messages.error(request, "You already have a CR profile!")
            return redirect('add_cr')
            

        name = request.POST.get('name')
        st_id = request.POST.get('st_id')
        university = request.POST.get('university')
        department = request.POST.get('department')
        batch = request.POST.get('batch')
        section = request.POST.get('section')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        bio = request.POST.get('bio')
        profile_picture = request.FILES.get('profile_picture')

        cr = CrProfile.objects.create(
            user=request.user,
            name=name,
            st_id=st_id,
            university=University.objects.get(id=university),
            department=Department.objects.get(id=department),
            batch=batch,
            section=section,
            email=email,
            phone=phone,
            bio=bio,
            profile_picture=profile_picture,
        )
        cr.save()
        
        messages.success(request, "CR profile added successfully!")

        return redirect('cr_profile', slug=cr.slug)

    context={
        'university':university,
        'department':department,

    }

    return render(request,'add_cr.html',context)
@login_required
def submit_review(request, cr_slug):
    cr_profile = get_object_or_404(CrProfile, slug=cr_slug)
    user = request.user

    # Check if the user already submitted a review for this CR
    existing_review = Review.objects.filter(user=user, cr_profile=cr_profile).first()
    if existing_review:
        messages.warning(request, "You have already reviewed this CR.")
        return redirect('submit_review')  # Redirect wherever you want

    if request.method == "POST":
        rating = request.POST.get('rating')
        description = request.POST.get('description', '')

        # Create review
        review = Review.objects.create(
            user=user,
            cr_profile=cr_profile,
            rating=int(rating),
            description=description
        )
        messages.success(request, "Your review has been submitted successfully!")
        return redirect('cr_profile', slug=cr_profile.slug) # Redirect after submission

    # If GET request, optionally show the modal/page
    return redirect('cr_profile', slug=cr_profile.slug)
