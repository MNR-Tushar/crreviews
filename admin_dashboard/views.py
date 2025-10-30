from django.shortcuts import get_object_or_404, redirect, render
from django.contrib import messages
from django.db.models import Count
from django.contrib.admin.views.decorators import staff_member_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from cr.models import *
from userprofile.models import *
from .forms import UniversityForm, DepartmentForm

@staff_member_required
def admin_dashboard(request):

    if not request.user.is_staff:
        messages.error(request, "You don't have permission to access this page.")
        return redirect('home')
    
   
    pending_count = Review.objects.filter(is_anonymous=True, is_approved=False).count()
    anonymous_reviews = Review.objects.filter(is_anonymous=True, is_approved=True).count()
    
   
    total_users = User.objects.count()
    total_crs = CrProfile.objects.count()
    total_reviews = Review.objects.count()
    total_universities = University.objects.count()
    total_departments = Department.objects.count()
    private_universities = University.objects.filter(type='Private').count()
    public_universities = University.objects.filter(type='Public').count()

    # Get page parameter for different sections
    users_page = request.GET.get('users_page', 1)
    crs_page = request.GET.get('crs_page', 1)
    reviews_page = request.GET.get('reviews_page', 1)
    universities_page = request.GET.get('universities_page', 1)
    departments_page = request.GET.get('departments_page', 1)
    pending_page = request.GET.get('page', 1)

    # Users Pagination
    users_list = User.objects.all().order_by('-created_at')
    users_paginator = Paginator(users_list, 10)
    try:
        users = users_paginator.page(users_page)
    except PageNotAnInteger:
        users = users_paginator.page(1)
    except EmptyPage:
        users = users_paginator.page(users_paginator.num_pages)

    # CRs Pagination
    crs_list = CrProfile.objects.all().order_by('-created_at')
    crs_paginator = Paginator(crs_list, 10)
    try:
        crs = crs_paginator.page(crs_page)
    except PageNotAnInteger:
        crs = crs_paginator.page(1)
    except EmptyPage:
        crs = crs_paginator.page(crs_paginator.num_pages)

    # Reviews Pagination
    reviews_list = Review.objects.all().order_by('-created_at')
    reviews_paginator = Paginator(reviews_list, 10)
    try:
        reviews = reviews_paginator.page(reviews_page)
    except PageNotAnInteger:
        reviews = reviews_paginator.page(1)
    except EmptyPage:
        reviews = reviews_paginator.page(reviews_paginator.num_pages)

    # Universities Pagination
    universities_list = University.objects.annotate(
        total_cr=Count('university_crs', distinct=True),
        total_review=Count('university_crs__cr_reviews', distinct=True),
        total_users=Count('university_user', distinct=True)
    ).order_by('-total_cr')
    universities_paginator = Paginator(universities_list, 9)  # 9 for grid layout
    try:
        univercities = universities_paginator.page(universities_page)
    except PageNotAnInteger:
        univercities = universities_paginator.page(1)
    except EmptyPage:
        univercities = universities_paginator.page(universities_paginator.num_pages)

    # Departments Pagination
    departments_list = Department.objects.annotate(
        total_cr=Count('department_crs', distinct=True),
        total_review=Count('department_crs__cr_reviews', distinct=True),
        total_users=Count('department_user', distinct=True)
    ).order_by('-total_cr')
    departments_paginator = Paginator(departments_list, 10)
    try:
        departments = departments_paginator.page(departments_page)
    except PageNotAnInteger:
        departments = departments_paginator.page(1)
    except EmptyPage:
        departments = departments_paginator.page(departments_paginator.num_pages)

    # Pending Reviews Pagination
    pending_list = Review.objects.filter(is_anonymous=True, is_approved=False).order_by('-created_at')
    pending_paginator = Paginator(pending_list, 10)
    try:
        pending = pending_paginator.page(pending_page)
    except PageNotAnInteger:
        pending = pending_paginator.page(1)
    except EmptyPage:
        pending = pending_paginator.page(pending_paginator.num_pages)
 
    
    context = {
        'pending_count': pending_count,
        'anonymous_reviews': anonymous_reviews,
        'total_users': total_users,
        'total_crs': total_crs,
        'total_reviews': total_reviews,
        'total_universities': total_universities,
        'total_departments': total_departments,
        'private_universities': private_universities,
        'public_universities': public_universities,
        'users': users,
        'crs': crs,
        'reviews': reviews,
        'univercities': univercities,
        'departments': departments,
        'pending_reviews': pending,
    }
    
    return render(request, 'admin_dashboard/admin_dashboard.html', context)


@staff_member_required
def add_university(request):
    """View to add a new university"""
    if request.method == 'POST':
        form = UniversityForm(request.POST)
        if form.is_valid():
            university = form.save()
            messages.success(request, f'University "{university.title}" has been added successfully!')
            return redirect('admin_dashboard')  # Redirect to dashboard
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = UniversityForm()
    
    context = {
        'form': form,
        'title': 'Add New University',
        'submit_text': 'Add University'
    }
    return render(request, 'admin_dashboard/add_university.html', context)


@staff_member_required
def edit_university(request, slug):
    """View to edit an existing university"""
    university = get_object_or_404(University, slug=slug)
    
    if request.method == 'POST':
        form = UniversityForm(request.POST, instance=university)
        if form.is_valid():
            university = form.save()
            messages.success(request, f'University "{university.title}" has been updated successfully!')
            return redirect('admin_dashboard')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = UniversityForm(instance=university)
    
    context = {
        'form': form,
        'title': f'Edit University: {university.title}',
        'submit_text': 'Update University',
        'university': university
    }
    return render(request, 'admin_dashboard/add_university.html', context)


@staff_member_required
def delete_university(request, slug):
  
    university = get_object_or_404(University, slug=slug)
    
  
    title = university.title
    university.delete()
    messages.success(request, f'University "{title}" has been deleted successfully!')
    return redirect('/admin_dashboard/')



@staff_member_required
def add_department(request):
    """View to add a new department"""
    if request.method == 'POST':
        form = DepartmentForm(request.POST)
        if form.is_valid():
            department = form.save()
            messages.success(request, f'Department "{department.title}" has been added successfully!')
            return redirect('admin_dashboard')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = DepartmentForm()
    
    context = {
        'form': form,
        'title': 'Add New Department',
        'submit_text': 'Add Department'
    }
    return render(request, 'admin_dashboard/add_department.html', context)


@staff_member_required
def edit_department(request, slug):
    """View to edit an existing department"""
    department = get_object_or_404(Department, slug=slug)
    
    if request.method == 'POST':
        form = DepartmentForm(request.POST, instance=department)
        if form.is_valid():
            department = form.save()
            messages.success(request, f'Department "{department.title}" has been updated successfully!')
            return redirect('admin_dashboard')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = DepartmentForm(instance=department)
    
    context = {
        'form': form,
        'title': f'Edit Department: {department.title}',
        'submit_text': 'Update Department',
        'department': department
    }
    return render(request, 'admin_dashboard/add_department.html', context)


@staff_member_required
def delete_department(request, slug):

    department = get_object_or_404(Department, slug=slug)
   
    title = department.title
    department.delete()
    messages.success(request, f'Department "{title}" has been deleted successfully!')
    return redirect('/admin_dashboard/')
   