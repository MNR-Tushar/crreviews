from django.contrib import messages
from django.shortcuts import render,redirect
from django.contrib.auth import get_user_model
from cr.models import *
from .models import *


def login(request):
    return render(request,'user_profile/login.html')


def registration(request):
    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        student_id = request.POST.get('student_id')
        university_id = request.POST.get('university')
        department_id = request.POST.get('department')
        password = request.POST.get('password')
        password2 = request.POST.get('password2')
        
        # Validation
        if password != password2:
            messages.error(request, 'Passwords do not match!')
            return redirect('registration')
        
        if User.objects.filter(email=email).exists():
            messages.error(request, 'Email already exists!')
            return redirect('registration')
        
        if User.objects.filter(student_id=student_id).exists():
            messages.error(request, 'Student ID already exists!')
            return redirect('registration')
        
        try:
            # Get university and department objects
            university = University.objects.get(id=university_id) if university_id else None
            department = Department.objects.get(id=department_id) if department_id else None
            
            # Create user
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
    
    # GET request
    universitys = University.objects.all()
    departments = Department.objects.all()
    
    context = {
        'universitys': universitys,
        'departments': departments,
    }
    
    return render(request, 'user_profile/registration.html', context)


def logout(request):
    pass

def user_dasboard(request):
    return render(request,'user_profile/user_dashboard.html')

def admin_dashboard(request):
    return render(request,'user_profile/admin_dashboard.html')