from django.contrib import messages
from django.shortcuts import render,redirect
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
def user_dasboard(request):
    user = User.objects.get(email=request.user.email)
    review = Review.objects.filter(user=user).order_by('-created_at')
    last = review.first()
 
    
    context = {
        'user':user,
        'review':review,
        'last':last,
    }

    return render(request,'user_profile/user_dashboard.html',context)
@login_required
def view_profile(request):
    user = User.objects.get(email=request.user.email)
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

@login_required
def admin_dashboard(request):
    return render(request,'user_profile/admin_dashboard.html')