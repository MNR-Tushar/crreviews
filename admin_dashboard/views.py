from django.shortcuts import get_object_or_404, redirect, render
from django.contrib import messages
from django.db.models import Count
from django.contrib.admin.views.decorators import staff_member_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import HttpResponseRedirect
from django.urls import reverse
from cr.models import *
from userprofile.models import *
from .forms import UniversityForm, DepartmentForm
from django.contrib.auth import get_user_model

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
  
    if request.method == 'POST':
        form = UniversityForm(request.POST)
        if form.is_valid():
            university = form.save()
            messages.success(request, f'University "{university.title}" has been added successfully!')
            return HttpResponseRedirect(reverse('admin_dashboard') + '#universities')
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
   
    university = get_object_or_404(University, slug=slug)
    
    if request.method == 'POST':
        form = UniversityForm(request.POST, instance=university)
        if form.is_valid():
            university = form.save()
            messages.success(request, f'University "{university.title}" has been updated successfully!')
            return HttpResponseRedirect(reverse('admin_dashboard') + '#universities')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = UniversityForm(instance=university)
    
    context = {
        'form': form,
        'title': university.title,
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
    return HttpResponseRedirect(reverse('admin_dashboard') + '#universities')
   


@staff_member_required
def add_department(request):
  
    if request.method == 'POST':
        form = DepartmentForm(request.POST)
        if form.is_valid():
            department = form.save()
            messages.success(request, f'Department "{department.title}" has been added successfully!')
            return HttpResponseRedirect(reverse('admin_dashboard') + '#departments')
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
   
    department = get_object_or_404(Department, slug=slug)
    
    if request.method == 'POST':
        form = DepartmentForm(request.POST, instance=department)
        if form.is_valid():
            department = form.save()
            messages.success(request, f'Department "{department.title}" has been updated successfully!')
            return HttpResponseRedirect(reverse('admin_dashboard') + '#departments')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = DepartmentForm(instance=department)
    
    context = {
        'form': form,
        'title': department.title,
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
    return HttpResponseRedirect(reverse('admin_dashboard') + '#departments')






User = get_user_model()

@staff_member_required
def admin_add_cr(request):
    """Admin view to add a new CR"""
    universities = University.objects.all().order_by('title')
    departments = Department.objects.all().order_by('title')
    users = User.objects.filter(user_profile__isnull=True).order_by('email')  # Users without CR profile

    if request.method == 'POST':
        user_id = request.POST.get('user')
        name = request.POST.get('name')
        gender = request.POST.get('gender')
        st_id = request.POST.get('st_id')
        university_id = request.POST.get('university')
        department_id = request.POST.get('department')
        batch = request.POST.get('batch')
        dept_batch = request.POST.get('dept_batch')
        section = request.POST.get('section')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        bio = request.POST.get('bio')
        cr_status = request.POST.get('cr_status')
        profile_picture = request.FILES.get('profile_picture')
        date_of_birth = request.POST.get('date_of_birth') or None

        facebook_url = request.POST.get('facebook_url') or 'https://www.facebook.com/'
        instagram_url = request.POST.get('instagram_url') or 'https://www.instagram.com/'
        linkedin_url = request.POST.get('linkedin_url') or 'https://www.linkedin.com/'

        try:
            user = User.objects.get(id=user_id)
            university = University.objects.get(id=university_id)
            department = Department.objects.get(id=department_id)

            cr = CrProfile.objects.create(
                user=user,
                name=name,
                gender=gender,
                st_id=st_id,
                university=university,
                department=department,
                batch=batch,
                dept_batch=dept_batch,
                section=section,
                email=email,
                phone=phone,
                bio=bio,
                cr_status=cr_status,
                profile_picture=profile_picture,
                date_of_birth=date_of_birth,
                facebook_url=facebook_url,
                instagram_url=instagram_url,
                linkedin_url=linkedin_url,
            )
            messages.success(request, f'CR Profile "{cr.name}" has been created successfully!')
            return HttpResponseRedirect(reverse('admin_dashboard') + '#crs')
        except Exception as e:
            messages.error(request, f'Error creating CR: {str(e)}')

    context = {
        'universities': universities,
        'departments': departments,
        'users': users,
        'title': 'Add New CR',
    }
    return render(request, 'admin_dashboard/add_cr_admin.html', context)


@staff_member_required
def admin_view_cr(request, slug):
    """Admin view to see CR details"""
    cr = get_object_or_404(CrProfile, slug=slug)
    reviews = Review.objects.filter(cr_profile=cr, is_approved=True).order_by('-created_at')[:5]

    total_reviews_count = Review.objects.filter(cr_profile=cr).count()
    approved_reviews_count = Review.objects.filter(cr_profile=cr, is_approved=True).count()
    pending_reviews_count = total_reviews_count - approved_reviews_count
    
    context = {
        'cr': cr,
        'reviews': reviews,
        'title': f'View CR: {cr.name}',
        'approved_reviews_count': approved_reviews_count,
        'total_reviews_count': total_reviews_count,
        'pending_reviews_count': pending_reviews_count,
    }
    return render(request, 'admin_dashboard/view_cr_admin.html', context)


@staff_member_required
def admin_edit_cr(request, slug):
    """Admin view to edit an existing CR"""
    cr = get_object_or_404(CrProfile, slug=slug)
    universities = University.objects.all().order_by('title')
    departments = Department.objects.all().order_by('title')

    if request.method == 'POST':
        cr.name = request.POST.get('name')
        cr.gender = request.POST.get('gender')
        cr.st_id = request.POST.get('st_id')
        cr.university = University.objects.get(id=request.POST.get('university'))
        cr.department = Department.objects.get(id=request.POST.get('department'))
        cr.batch = request.POST.get('batch')
        cr.dept_batch = request.POST.get('dept_batch')
        cr.section = request.POST.get('section')
        cr.email = request.POST.get('email')
        cr.phone = request.POST.get('phone')
        cr.bio = request.POST.get('bio')
        cr.cr_status = request.POST.get('cr_status')
        cr.date_of_birth = request.POST.get('date_of_birth') or None

        cr.facebook_url = request.POST.get('facebook_url') or 'https://www.facebook.com/'
        cr.instagram_url = request.POST.get('instagram_url') or 'https://www.instagram.com/'
        cr.linkedin_url = request.POST.get('linkedin_url') or 'https://www.linkedin.com/'

        new_picture = request.FILES.get('profile_picture')
        if new_picture:
            cr.profile_picture = new_picture

        cr.save()
        messages.success(request, f'CR Profile "{cr.name}" has been updated successfully!')
        return HttpResponseRedirect(reverse('admin_dashboard') + '#crs')

    context = {
        'cr': cr,
        'universities': universities,
        'departments': departments,
        'title': f'Edit CR: {cr.name}',
    }
    return render(request, 'admin_dashboard/add_cr_admin.html', context)


@staff_member_required
def admin_delete_cr(request, slug):
    """Admin view to delete a CR"""
    cr = get_object_or_404(CrProfile, slug=slug)
    cr_name = cr.name
    cr.delete()
    messages.success(request, f'CR Profile "{cr_name}" has been deleted successfully!')
    return HttpResponseRedirect(reverse('admin_dashboard') + '#crs')


@staff_member_required
def admin_view_review(request, slug):
    """Admin view to see review details"""
    review = get_object_or_404(Review, slug=slug)
    
    context = {
        'review': review,
        'title': f'View Review: {review.cr_profile.name}',
    }
    return render(request, 'admin_dashboard/view_review_admin.html', context)


@staff_member_required
def admin_edit_review(request, slug):
    """Admin view to edit an existing review"""
    review = get_object_or_404(Review, slug=slug)

    if request.method == 'POST':
        rating = request.POST.get('rating')
        description = request.POST.get('description', '').strip()
        
        try:
            review.rating = int(rating)
            review.description = description
            review.save()
            
            messages.success(request, f'Review for "{review.cr_profile.name}" has been updated successfully!')
            return HttpResponseRedirect(reverse('admin_dashboard') + '#reviews')
        except Exception as e:
            messages.error(request, f'Error updating review: {str(e)}')

    context = {
        'review': review,
        'title': f'Edit Review: {review.cr_profile.name}',
    }
    return render(request, 'admin_dashboard/edit_review_admin.html', context)


@staff_member_required
def admin_delete_review(request, slug):
    """Admin view to delete a review"""
    review = get_object_or_404(Review, slug=slug)
    cr_name = review.cr_profile.name
    reviewer_name = review.get_reviewer_name()
    
    review.delete()
    messages.success(request, f'Review by "{reviewer_name}" for "{cr_name}" has been deleted successfully!')
    return HttpResponseRedirect(reverse('admin_dashboard') + '#reviews')


# Add these functions to your admin_dashboard/views.py file

@staff_member_required
def admin_view_user(request, slug):
    """Admin view to see user details"""
    user = get_object_or_404(User, slug=slug)
    reviews = Review.objects.filter(user=user, is_approved=True).order_by('-created_at')[:5]
    saved_crs = SavedCR.objects.filter(user=user).select_related('cr_profile')[:5]
    
    total_reviews_count = Review.objects.filter(user=user).count()
    approved_reviews_count = Review.objects.filter(user=user, is_approved=True).count()
    pending_reviews_count = total_reviews_count - approved_reviews_count
    saved_crs_count = saved_crs.count()
    
    context = {
        'view_user': user,
        'reviews': reviews,
        'saved_crs': saved_crs,
        'title': f'View User: {user.get_full_name()}',
        'total_reviews_count': total_reviews_count,
        'approved_reviews_count': approved_reviews_count,
        'pending_reviews_count': pending_reviews_count,
        'saved_crs_count': saved_crs_count,
    }
    return render(request, 'admin_dashboard/view_user_admin.html', context)


@staff_member_required
def admin_edit_user(request, slug):
    """Admin view to edit an existing user"""
    user = get_object_or_404(User, slug=slug)
    universities = University.objects.all().order_by('title')
    departments = Department.objects.all().order_by('title')

    if request.method == 'POST':
        user.first_name = request.POST.get('first_name')
        user.last_name = request.POST.get('last_name')
        user.email = request.POST.get('email')
        user.student_id = request.POST.get('student_id')
        user.gender = request.POST.get('gender')
        user.phone = request.POST.get('phone')
        user.batch = request.POST.get('batch')
        user.dept_batch = request.POST.get('dept_batch')
        user.section = request.POST.get('section')
        user.bio = request.POST.get('bio')
        user.date_of_birth = request.POST.get('date_of_birth') or None
        
        user.facebook_url = request.POST.get('facebook_url') or 'https://www.facebook.com/'
        user.instagram_url = request.POST.get('instagram_url') or 'https://www.instagram.com/'
        user.linkedin_url = request.POST.get('linkedin_url') or 'https://www.linkedin.com/'
        
        # Handle profile picture
        new_picture = request.FILES.get('profile_picture')
        if new_picture:
            user.profile_picture = new_picture
        
        # Handle university and department
        university_id = request.POST.get('university')
        department_id = request.POST.get('department')
        
        if university_id:
            user.university = University.objects.get(id=university_id)
        if department_id:
            user.department = Department.objects.get(id=department_id)
        
        # Handle user status
        is_active = request.POST.get('is_active') == 'on'
        is_email_verified = request.POST.get('is_email_verified') == 'on'
        
        user.is_active = is_active
        user.is_email_verified = is_email_verified
        
        user.save()
        messages.success(request, f'User "{user.get_full_name()}" has been updated successfully!')
        return HttpResponseRedirect(reverse('admin_dashboard') + '#users')

    context = {
        'view_user': user,
        'universities': universities,
        'departments': departments,
        'title': f'Edit User: {user.get_full_name()}',
    }
    return render(request, 'admin_dashboard/edit_user_admin.html', context)


@staff_member_required
def admin_delete_user(request, slug):
    """Admin view to delete a user"""
    user = get_object_or_404(User, slug=slug)
    
    # Prevent deleting superusers or staff members
    if user.is_superuser or user.is_staff:
        messages.error(request, 'Cannot delete admin or staff users!')
        return HttpResponseRedirect(reverse('admin_dashboard') + '#users')
    
    user_name = user.get_full_name()
    user.delete()
    messages.success(request, f'User "{user_name}" has been deleted successfully!')
    return HttpResponseRedirect(reverse('admin_dashboard') + '#users')