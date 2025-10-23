
from django.contrib import messages
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .models import *
from userprofile.models import *
from django.contrib.auth.decorators import login_required
from django.db.models import Q, Avg

def home(request):

    search_quary = request.GET.get('search')
    university_filter = request.GET.get('university')
    department_filter = request.GET.get('department')

    
 
    cr=CrProfile.objects.all()
   

    if search_quary:
        cr = cr.filter(
            Q(name__icontains=search_quary)|
            Q(st_id__icontains=search_quary)|
            Q(email__icontains=search_quary)
            
        )
    if university_filter:
        cr = cr.filter(university__id=university_filter)
    if department_filter:
        cr = cr.filter(department__id=department_filter)

    cr=cr.order_by('-created_at')
    total_university=University.objects.count()
    total_department=Department.objects.count()
    total_review=Review.objects.count()
    crs = sorted(
    CrProfile.objects.all(),
    key=lambda x: x.average_rating,
    reverse=True
    )

    universities = University.objects.all()
    departments = Department.objects.all()

    context={
        'cr':cr,
        'total_university':total_university,
        'total_department':total_department,
        'total_review':total_review,
        'crs':crs,
        'universities':universities,
        'departments':departments,
        'university_filter':university_filter,
        'department_filter':department_filter,

        
    }
    return render(request,'home.html',context)

def all_cr(request):

    search_query = request.GET.get('search')
    university_filter = request.GET.get('university')
    department_filter = request.GET.get('department')
    rating_filter = request.GET.get('rating')


    crs = CrProfile.objects.all()

    if search_query:
        crs = crs.filter(
            Q(name__icontains=search_query) |
            Q(st_id__icontains=search_query) |
            Q(email__icontains=search_query)|
            Q(batch__icontains=search_query)|
            Q(dept_batch__icontains=search_query)|
            Q(section__icontains=search_query)
        )

    if university_filter:
        crs = crs.filter(university__id=university_filter)
    if department_filter:
        crs = crs.filter(department__id=department_filter)

    if rating_filter:
        filtered_crs = []
        for cr in crs:
            avg_rating = cr.average_rating
            if rating_filter == '5' and avg_rating >= 4.5:
                filtered_crs.append(cr)
            elif rating_filter == '4' and 3.5 <= avg_rating < 4.5:
                filtered_crs.append(cr)
            elif rating_filter == '3' and 2.5 <= avg_rating < 3.5:
                filtered_crs.append(cr)
            elif rating_filter == '2' and 1.5 <= avg_rating < 2.5:
                filtered_crs.append(cr)
            elif rating_filter == '1' and avg_rating < 1.5:
                filtered_crs.append(cr)
        crs = filtered_crs
    else:
        crs = crs.order_by('-created_at')

    
    paginator = Paginator(crs, 9)
    page_number =  request.GET.get('page',1)

    try:
        crs = paginator.page(page_number)
    except PageNotAnInteger:
        crs = paginator.page(1)
    except EmptyPage:
        crs = paginator.page(1)

    universities = University.objects.all()
    departments = Department.objects.all()

    context={
        'cr':crs,
        'paginator':paginator,
        'universities':universities,
        'departments':departments,
        'university_filter':university_filter,
        'department_filter':department_filter,
        'rating_filter':rating_filter,
       
        
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


    is_saved = False
    if request.user.is_authenticated:
        is_saved = cr_profile.saved_by.filter(user=request.user).exists()

    context={
        'cr_profile':cr_profile,
        'review':review,
        'paginator':paginator,
        'is_saved':is_saved

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
        gender = request.POST.get('gender')
        st_id = request.POST.get('st_id')
        university = request.POST.get('university')
        department = request.POST.get('department')
        batch = request.POST.get('batch')
        dept_batch = request.POST.get('dept_batch')
        section = request.POST.get('section')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        bio = request.POST.get('bio')
        profile_picture = request.FILES.get('profile_picture')

        cr = CrProfile.objects.create(
            user=request.user,
            name=name,
            gender=gender,
            st_id=st_id,
            university=University.objects.get(id=university),
            department=Department.objects.get(id=department),
            batch=batch,
            dept_batch=dept_batch,
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
def edit_cr_profile(request,slug):

    cr=get_object_or_404(CrProfile,slug=slug,user=request.user)
    university = University.objects.all()
    department = Department.objects.all()

    if request.method == 'POST':
        cr.name = request.POST.get('name')
        cr.st_id = request.POST.get('st_id')
        cr.gender = request.POST.get('gender')
        cr.date_of_birth = request.POST.get('date_of_birth')
        cr.university = University.objects.get(id=request.POST.get('university'))
        cr.department = Department.objects.get(id=request.POST.get('department'))
        cr.batch = request.POST.get('batch')
        cr.dept_batch = request.POST.get('dept_batch')
        cr.section = request.POST.get('section')
        cr.email = request.POST.get('email')
        cr.phone = request.POST.get('phone')
        cr.bio = request.POST.get('bio')

        cr.facebook_url = request.POST.get('facebook_url')
        cr.instagram_url = request.POST.get('instagram_url')
        cr.linkedin_url = request.POST.get('linkedin_url')

        new_picture = request.FILES.get('profile_picture')
        if new_picture:
            cr.profile_picture = new_picture
        cr.save()
        messages.success(request, "CR profile updated successfully!")
        return redirect('user_dashboard', slug=cr.user.slug)



    context={
        'cr':cr,
        'university':university,
        'department':department,
    }
    return render(request,'edit_cr_modal.html',context)


@login_required
def delete_cr_profile(request, slug):
    cr = get_object_or_404(CrProfile, slug=slug, user=request.user)
    
    if request.method == 'POST':
        cr_name = cr.name
        cr.delete()
        
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({
                'success': True,
                'message': f'CR profile "{cr_name}" deleted successfully!'
            })
        else:
            messages.success(request, f'CR profile deleted successfully!')
            return redirect('user_dashboard')
    
    return redirect('user_dashboard')



def submit_review(request, cr_slug):
    cr_profile = get_object_or_404(CrProfile, slug=cr_slug)
    user = request.user

    if user.is_anonymous:
        messages.error(request, "You must be logged in to submit a review.")
        return redirect('cr_profile', slug=cr_profile.slug)

    # Check if the user already submitted a review
    existing_review = Review.objects.filter(user=user).first()
    if existing_review:
        messages.warning(request, "You have already reviewed a CR. You can only review once!")
        return redirect('cr_profile', slug=cr_profile.slug)

    if request.method == "POST":
        rating = request.POST.get('rating')
        description = request.POST.get('description', '')

        try:
            review = Review.objects.create(
                user=user,
                cr_profile=cr_profile,
                rating=int(rating),
                description=description
            )
            messages.success(request, "Your review has been submitted successfully!")
            return redirect('cr_profile', slug=cr_profile.slug)
        except Exception as e:
            messages.error(request, "Error submitting review. Please try again.")
            return redirect('cr_profile', slug=cr_profile.slug)

    return redirect('cr_profile', slug=cr_profile.slug)

@login_required
def edit_review(request,slug):
    review = get_object_or_404(Review,slug=slug,user=request.user)

    if review.user != request.user:
        messages.error(request, "You do not have permission to edit this review.")
        return redirect('user_dashboard',slug=request.user.slug)

    if request.method == 'POST':
        rating = request.POST.get('rating')
        description = request.POST.get('description', '')

        try:
            review.rating = int(rating)
            review.description = description
            review.save()
            messages.success(request, "Your review has been updated successfully!")
            return redirect('user_dashboard',slug=request.user.slug)
        except Exception as e:
            messages.error(request, "Error updating review. Please try again.")
            return redirect('user_dashboard',slug=request.user.slug)

    return render(request, 'user_profile/user_dashboard.html')

@login_required
def delete_review(request,slug):
    review = get_object_or_404(Review,slug=slug,user=request.user)

    if review.user != request.user:
        messages.error(request, "You do not have permission to delete this review.")
        return redirect('user_dashboard',slug=request.user.slug)

    
    review.delete()
    messages.success(request, "Your review has been deleted successfully!")
    return redirect('user_dashboard',slug=request.user.slug)
