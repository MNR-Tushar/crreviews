from django.contrib import messages
from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth import authenticate,login as auth_login,logout as auth_logout
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from cr.models import *
from .models import *
from django.contrib.auth.decorators import login_required

def login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        
        user = authenticate(request, email=email, password=password)
        
        if user is not None:
            auth_login(request, user)
            messages.success(request, 'Successfully logged in!')
            return redirect('home')
        else:
            messages.error(request, 'Invalid email or password!')
            return redirect('login')
    
    return render(request, 'user_profile/login.html')


def registration(request):

    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        student_id = request.POST.get('student_id')
        university_id = request.POST.get('university')
        department_id = request.POST.get('department')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        
        
        if password != confirm_password:
            messages.error(request, 'Passwords do not match!')
            return redirect('registration')
        
        if User.objects.filter(email=email).exists():
            messages.error(request, 'Email already exists!')
            return redirect('registration')
        
        if User.objects.filter(student_id=student_id).exists():
            messages.error(request, 'Student ID already exists!')
            return redirect('registration')
        
        try:
            
            university = University.objects.get(id=university_id) if university_id else None
            department = Department.objects.get(id=department_id) if department_id else None
            
            
            user = User.objects.create_user(
                first_name=first_name,
                last_name=last_name,
                email=email,
                password=password,
                student_id=student_id,
                university=university,
                department=department
            )
            
            messages.success(request, 'Registration successful! Please login.')
            return redirect('login')
            
        except Exception as e:
            messages.error(request, f'Registration failed: {str(e)}')
            return redirect('registration')
    
    
    universitys = University.objects.all()
    departments = Department.objects.all()
    
    context = {
        'universitys': universitys,
        'departments': departments,
    }
    
    return render(request, 'user_profile/registration.html', context)


def logout(request):
    auth_logout(request)
    return redirect('login')

@login_required
def user_dasboard(request,slug):
    user = User.objects.get(email=request.user.email,slug=slug)
    review = Review.objects.filter(user=user).order_by('-created_at')
    saved_crs = SavedCR.objects.filter(user=request.user).select_related('cr_profile')
    last = review.first()
    last_cr_saved= saved_crs.last()
 
    
    context = {
        'user':user,
        'review':review,
        'last':last,
        'saved_crs':saved_crs,
        'last_cr_saved':last_cr_saved,
    }

    return render(request,'user_profile/user_dashboard.html',context)

def view_profile(request,slug):
    user = User.objects.get(email=request.user.email,slug=slug)
    review = Review.objects.filter(user=user).order_by('-created_at')

    paginator = Paginator(review,5)
    page_number = request.GET.get('page',1)

    try:
        review = paginator.page(page_number)
    except PageNotAnInteger:
        review = paginator.page(1)
    except EmptyPage:
        review = paginator.page(1)

    context = {
        'user':user,
        'review':review,
    }
    
    return render(request,'user_profile/view_profile.html',context)

def user_view(request,slug):
    view_user =get_object_or_404(User,slug=slug)
    review = Review.objects.filter(user=view_user).order_by('-created_at')

    paginator = Paginator(review,5)
    page_number = request.GET.get('page',1)

    try:
        review = paginator.page(page_number)
    except PageNotAnInteger:
        review = paginator.page(1)
    except EmptyPage:
        review = paginator.page(1)
    
    context = {
        'view_user':view_user,
        'user': request.user,
        'review':review
    }
    

    return render(request,'user_profile/user_view.html',context)

@login_required
def admin_dashboard(request):
    return render(request,'user_profile/admin_dashboard.html')

@login_required
def edit_user(request,slug):

    user = get_object_or_404(User,slug=slug)
    university = University.objects.all()
    department = Department.objects.all()

    if request.user != user:
        messages.error(request, "You are not authorized to edit this profile.")
        return redirect('home')
    

    if request.method == 'POST':
            user.first_name = request.POST.get('first_name')
            user.last_name = request.POST.get('last_name')
            user.email = request.POST.get('email')
            user.student_id = request.POST.get('student_id')
            user.batch = request.POST.get('batch')
            user.section = request.POST.get('section')
            user.bio = request.POST.get('bio')
            user.gender = request.POST.get('gender')
            user.date_of_birth = request.POST.get('date_of_birth')
            new_picture = request.FILES.get('profile_picture')
            if new_picture:
                user.profile_picture = new_picture

            user.phone = request.POST.get('phone')

            user.facebook_url = request.POST.get('facebook_url' '')
            user.instagram_url = request.POST.get('instagram_url')
            user.linkedin_url = request.POST.get('linkedin_url')

            university_id = request.POST.get('university')
            department_id = request.POST.get('department')

            if university_id:
                user.university = University.objects.get(id=university_id)
            if department_id:
                user.department = Department.objects.get(id=department_id)
            

            user.save()
            messages.success(request, 'Profile updated successfully!')
            return redirect('edit_user', slug=user.slug)

    context = {
            'user':request.user,
            'university':university,
            'department':department,
        }

    return render(request,'user_profile/edit_user.html',context)

def settings(request):

    return render(request,'user_profile/settings.html')




@login_required
def save_cr(request, slug):
    cr_profile = get_object_or_404(CrProfile, slug=slug)
    saved, created = SavedCR.objects.get_or_create(user=request.user, cr_profile=cr_profile)

    if created:
        messages.success(request, f"{cr_profile.name} saved to your favorites!")
    else:
        messages.info(request, f"{cr_profile.name} is already in your saved list.")

    return redirect('cr_profile', slug=slug)

@login_required
def remove_saved_cr(request, slug):
    cr_profile = get_object_or_404(CrProfile, slug=slug)
    SavedCR.objects.filter(user=request.user, cr_profile=cr_profile).delete()
    messages.success(request, f"{cr_profile.name} removed from your saved list.")
    return redirect('cr_profile', slug=slug)


