from django.contrib import messages
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .models import *
from userprofile.models import *
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.utils import timezone
from django.contrib.admin.views.decorators import staff_member_required

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
    total_user=User.objects.count()
    total_review = Review.objects.filter(is_approved=True).count()
    total_anonymous_reviews = Review.objects.filter(is_anonymous=True, is_approved=True).count()
    pending_anonymous_reviews = Review.objects.filter(is_anonymous=True, is_approved=False).count()
    approved_reviews = total_review
    pending_reviews = pending_anonymous_reviews

    crs = sorted(
    CrProfile.objects.all(),
    key=lambda x: x.average_rating,
    reverse=True
    )

    universities = University.objects.all().order_by('title')
    departments = Department.objects.all().order_by('title')
    active_notices = Notice.objects.filter(is_active=True)

    rating_distribution = {
        5: 0,
        4: 0,
        3: 0,
        2: 0,
        1: 0
    }
    
    all_crs = CrProfile.objects.all()
    total_crs_with_ratings = 0
    
    for cr_item in all_crs:
        avg_rating = cr_item.average_rating
        if avg_rating > 0:
            total_crs_with_ratings += 1
            if avg_rating >= 4.5:
                rating_distribution[5] += 1
            elif avg_rating >= 3.5:
                rating_distribution[4] += 1
            elif avg_rating >= 2.5:
                rating_distribution[3] += 1
            elif avg_rating >= 1.5:
                rating_distribution[2] += 1
            else:
                rating_distribution[1] += 1
    
    
    rating_percentages = {}
    if total_crs_with_ratings > 0:
        for star, count in rating_distribution.items():
            rating_percentages[star] = round((count / total_crs_with_ratings) * 100, 1)
    else:
        rating_percentages = {5: 0, 4: 0, 3: 0, 2: 0, 1: 0}

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
        'rating_distribution': rating_distribution,
        'rating_percentages': rating_percentages,
        'active_notices':active_notices,
        'approved_reviews':approved_reviews,
        'pending_reviews':pending_reviews,
        'total_anonymous_reviews':total_anonymous_reviews,
        'total_user':total_user,

        
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

    universities = University.objects.all().order_by('title')
    departments = Department.objects.all().order_by('title')

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
    reviews = Review.objects.filter(is_approved=True).order_by('-created_at')
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
    review = Review.objects.filter(cr_profile=cr_profile, is_approved=True).order_by('-created_at')


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

    university = University.objects.all().order_by('title')
    department = Department.objects.all().order_by('title')

    if request.method == 'POST':

       
        if hasattr(request.user, 'user_profile'):
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
        cr_status = request.POST.get('cr_status')

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
            cr_status=cr_status,
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
    university = University.objects.all().order_by('title')
    department = Department.objects.all().order_by('title')

    if request.method == 'POST':
        cr.name = request.POST.get('name')
        cr.st_id = request.POST.get('st_id')
        cr.gender = request.POST.get('gender')
        cr.date_of_birth = request.POST.get('date_of_birth') or None
        cr.university = University.objects.get(id=request.POST.get('university'))
        cr.department = Department.objects.get(id=request.POST.get('department'))
        cr.batch = request.POST.get('batch')
        cr.dept_batch = request.POST.get('dept_batch')
        cr.section = request.POST.get('section')
        cr.email = request.POST.get('email')
        cr.phone = request.POST.get('phone')
        cr.bio = request.POST.get('bio')
        cr.cr_status = request.POST.get('cr_status')

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

    if not request.user.is_authenticated:
        messages.error(request, "You must be logged in to submit a review!")
        return redirect('login')
        

    if request.method == "POST":
        rating = request.POST.get('rating')
        description = request.POST.get('description', '').strip()
        is_anonymous = request.POST.get('is_anonymous') == 'on'

   
        if not rating:
            messages.error(request, "Please select a rating!")
            return redirect('cr_profile', slug=cr_profile.slug)

        try:
            rating = int(rating)
            if rating < 1 or rating > 5:
                messages.error(request, "Invalid rating value!")
                return redirect('cr_profile', slug=cr_profile.slug)
        except ValueError:
            messages.error(request, "Invalid rating value!")
            return redirect('cr_profile', slug=cr_profile.slug)

    
        if request.user.is_authenticated:
          
            existing_review = Review.objects.filter(
                user=request.user,
                cr_profile=cr_profile
            ).first()

            if existing_review:
                messages.warning(request, "You have already reviewed this CR!")
                return redirect('cr_profile', slug=cr_profile.slug)

      
            try:
           
                is_approved = not is_anonymous  
            
                Review.objects.create(
                user=request.user,
                cr_profile=cr_profile,
                rating=rating,
                description=description,
                is_anonymous=is_anonymous,
                anonymous_name=request.user.get_full_name() if is_anonymous else None,
                is_approved=is_approved,
            )
            
                if is_anonymous:
                    messages.success(request, "Your anonymous review has been submitted and is pending admin approval!")
                else:
                    messages.success(request, "Your review has been submitted successfully!")
            except Exception as e:
                messages.error(request, f"Error submitting review: {str(e)}")

        
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



@staff_member_required
def pending_reviews(request):
   
    pending = Review.objects.filter(is_anonymous=True, is_approved=False).order_by('-created_at')
    
    paginator = Paginator(pending, 10)
    page_number = request.GET.get('page', 1)
    
    try:
        pending = paginator.page(page_number)
    except PageNotAnInteger:
        pending = paginator.page(1)
    except EmptyPage:
        pending = paginator.page(1)
    
    context = {
        'pending_reviews': pending,
        'paginator': paginator,
    }
    return render(request, 'review_status/pending_reviews.html', context)

@staff_member_required
def approve_review(request, slug):
    
    review = get_object_or_404(Review, slug=slug, is_anonymous=True)
    
    if request.method == 'POST':
        review.is_approved = True
        review.reviewed_by = request.user
        review.reviewed_at = timezone.now()
        review.save()
        
        messages.success(request, f"Review approved successfully!")
        return redirect('pending_reviews')
    
    return redirect('pending_reviews')

@staff_member_required
def reject_review(request, slug):
    
    review = get_object_or_404(Review, slug=slug, is_anonymous=True)
    
    if request.method == 'POST':
        cr_name = review.cr_profile.name
        review.delete()
        
        messages.success(request, f"Review for {cr_name} has been rejected and deleted!")
        return redirect('pending_reviews')
    
    return redirect('pending_reviews')