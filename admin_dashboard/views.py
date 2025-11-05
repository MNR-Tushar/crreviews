from django.shortcuts import get_object_or_404, redirect, render
from django.contrib import messages
from django.db.models import Count
from django.contrib.admin.views.decorators import staff_member_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import HttpResponseRedirect
from django.urls import reverse
from cr.models import *
from userprofile.models import *
from .models import *
from .forms import UniversityForm, DepartmentForm
from django.contrib.auth import get_user_model
from django.db.models.functions import TruncMonth
from django.utils import timezone
from datetime import timedelta
import json

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

    # Add these new counts
    total_notices = Notice.objects.count()
    active_notices = Notice.objects.filter(is_active=True).count()
    total_messages = ContactMessage.objects.count()
    unread_messages = ContactMessage.objects.filter(is_read=False).count()

    # Developer Profile counts
    total_developers = Developer_Profile.objects.count()
    total_tech_stack = Teck_Stack.objects.count()
    
    # Monthly Statistics - Last 6 months
    six_months_ago = timezone.now() - timedelta(days=180)
    
    # CRs per month
    cr_monthly = CrProfile.objects.filter(
        created_at__gte=six_months_ago
    ).annotate(
        month=TruncMonth('created_at')
    ).values('month').annotate(
        count=Count('id')
    ).order_by('month')
    
    # Reviews per month
    review_monthly = Review.objects.filter(
        created_at__gte=six_months_ago
    ).annotate(
        month=TruncMonth('created_at')
    ).values('month').annotate(
        count=Count('id')
    ).order_by('month')
    
    # Users per month
    user_monthly = User.objects.filter(
        created_at__gte=six_months_ago
    ).annotate(
        month=TruncMonth('created_at')
    ).values('month').annotate(
        count=Count('id')
    ).order_by('month')
    
    # Format data for chart
    def format_monthly_data(queryset):
        data = []
        max_count = max([item['count'] for item in queryset], default=1)
        for item in queryset:
            data.append({
                'month': item['month'].strftime('%Y-%m'),
                'month_name': item['month'].strftime('%b'),
                'count': item['count'],
                'percentage': (item['count'] / max_count * 100) if max_count > 0 else 0
            })
        return data
    
    monthly_stats = {
        'crs': json.dumps(format_monthly_data(cr_monthly)),
        'reviews': json.dumps(format_monthly_data(review_monthly)),
        'users': json.dumps(format_monthly_data(user_monthly)),
    }

    # print(monthly_stats)
    # print(monthly_stats['crs'])

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
        'total_notices': total_notices,
        'active_notices': active_notices,
        'total_messages': total_messages,
        'unread_messages': unread_messages,
        'notices': Notice.objects.all()[:5],  
        'contact_messages': ContactMessage.objects.all()[:10],
        'developer_profiles': Developer_Profile.objects.all()[:3],
        'tech_stack_list': Teck_Stack.objects.all(),
        'monthly_stats': monthly_stats,
        'total_developers': total_developers,
        'total_tech_stack': total_tech_stack,

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




# Add after your existing views

@staff_member_required
def manage_notices(request):
    """View to manage notices"""
    notices = Notice.objects.all().order_by('-created_at')
    
    context = {
        'notices': notices,
    }
    return render(request, 'admin_dashboard/manage_notices.html', context)

@staff_member_required
def add_notice(request):
    """Add new notice"""
    if request.method == 'POST':
        title = request.POST.get('title')
        message = request.POST.get('message')
        notice_type = request.POST.get('notice_type')
        link = request.POST.get('link')
        is_active = request.POST.get('is_active') == 'on'
        
        Notice.objects.create(
            title=title,
            message=message,
            notice_type=notice_type,
            link=link,
            is_active=is_active
        )
        messages.success(request, 'Notice created successfully!')
        return redirect('admin_dashboard')
    
    return render(request, 'admin_dashboard/add_notice.html')

@staff_member_required
def edit_notice(request, pk):
    """Edit existing notice"""
    notice = get_object_or_404(Notice, pk=pk)
    
    if request.method == 'POST':
        notice.title = request.POST.get('title')
        notice.message = request.POST.get('message')
        notice.notice_type = request.POST.get('notice_type')
        notice.link = request.POST.get('link')
        notice.is_active = request.POST.get('is_active') == 'on'
        notice.save()
        
        messages.success(request, 'Notice updated successfully!')
        return redirect('admin_dashboard')
    
    context = {'notice': notice}
    return render(request, 'admin_dashboard/edit_notice.html', context)

@staff_member_required
def delete_notice(request, pk):
    """Delete notice"""
    notice = get_object_or_404(Notice, pk=pk)
    notice.delete()
    messages.success(request, 'Notice deleted successfully!')
    return redirect('admin_dashboard')

@staff_member_required
def toggle_notice(request, pk):
    """Toggle notice active status"""
    notice = get_object_or_404(Notice, pk=pk)
    notice.is_active = not notice.is_active
    notice.save()
    status = "activated" if notice.is_active else "deactivated"
    messages.success(request, f'Notice {status} successfully!')
    return redirect('admin_dashboard')

@staff_member_required
def view_messages(request):
    """View contact messages"""
    messages_list = ContactMessage.objects.all().order_by('-created_at')
    
    # Pagination
    page = request.GET.get('page', 1)
    paginator = Paginator(messages_list, 10)
    
    try:
        contact_messages = paginator.page(page)
    except PageNotAnInteger:
        contact_messages = paginator.page(1)
    except EmptyPage:
        contact_messages = paginator.page(paginator.num_pages)
    
    context = {
        'contact_messages': contact_messages,
    }
    return render(request, 'admin_dashboard/view_messages.html', context)

@staff_member_required
def mark_message_read(request, pk):
    """Mark message as read"""
    message = get_object_or_404(ContactMessage, pk=pk)
    message.is_read = True
    message.save()
    messages.success(request, 'Message marked as read!')
    return redirect('admin_dashboard')

@staff_member_required
def delete_message(request, pk):
    """Delete contact message"""
    message = get_object_or_404(ContactMessage, pk=pk)
    message.delete()
    messages.success(request, 'Message deleted successfully!')
    return redirect('admin_dashboard')

# Developer Profile Management
@staff_member_required
def add_developer_profile(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        degisnation = request.POST.get('degisnation')
        about = request.POST.get('about')
        years_of_experience = request.POST.get('years_of_experience') or None
        projects_built = request.POST.get('projects_built') or None
        location = request.POST.get('location')
        phone = request.POST.get('phone')
        email = request.POST.get('email')
        github_url = request.POST.get('github_url')
        linkedin_url = request.POST.get('linkedin_url')
        facebook_url = request.POST.get('facebook_url')
        twitter_url = request.POST.get('twitter_url')
        profile_picture = request.FILES.get('profile_picture')
        
        tech_stack_ids = request.POST.getlist('tech_stack')
        
        developer = Developer_Profile.objects.create(
            name=name,
            degisnation=degisnation,
            about=about,
            years_of_experience=years_of_experience,
            projects_built=projects_built,
            location=location,
            phone=phone,
            email=email,
            github_url=github_url,
            linkedin_url=linkedin_url,
            facebook_url=facebook_url,
            twitter_url=twitter_url,
            profile_picture=profile_picture
        )
        
        if tech_stack_ids:
            developer.tack_stack.set(tech_stack_ids)
        
        messages.success(request, f'Developer profile for {name} created successfully!')
        return HttpResponseRedirect(reverse('admin_dashboard') + '#developers')
    
    tech_stacks = Teck_Stack.objects.all()
    context = {'tech_stacks': tech_stacks}
    return render(request, 'admin_dashboard/add_developer_profile.html', context)


@staff_member_required
def edit_developer_profile(request, pk):
    developer = get_object_or_404(Developer_Profile, pk=pk)
    
    if request.method == 'POST':
        developer.name = request.POST.get('name')
        developer.degisnation = request.POST.get('degisnation')
        developer.about = request.POST.get('about')
        developer.years_of_experience = request.POST.get('years_of_experience') or None
        developer.projects_built = request.POST.get('projects_built') or None
        developer.location = request.POST.get('location')
        developer.phone = request.POST.get('phone')
        developer.email = request.POST.get('email')
        developer.github_url = request.POST.get('github_url')
        developer.linkedin_url = request.POST.get('linkedin_url')
        developer.facebook_url = request.POST.get('facebook_url')
        developer.twitter_url = request.POST.get('twitter_url')
        
        new_picture = request.FILES.get('profile_picture')
        if new_picture:
            developer.profile_picture = new_picture
        
        tech_stack_ids = request.POST.getlist('tech_stack')
        if tech_stack_ids:
            developer.tack_stack.set(tech_stack_ids)
        
        developer.save()
        messages.success(request, f'Developer profile for {developer.name} updated successfully!')
        return HttpResponseRedirect(reverse('admin_dashboard') + '#developers')
    
    tech_stacks = Teck_Stack.objects.all()
    context = {
        'developer': developer,
        'tech_stacks': tech_stacks
    }
    return render(request, 'admin_dashboard/edit_developer_profile.html', context)


@staff_member_required
def view_developer_profile(request, pk):
    developer = get_object_or_404(Developer_Profile, pk=pk)
    context = {'developer': developer}
    return render(request, 'admin_dashboard/view_developer_profile.html', context)


@staff_member_required
def delete_developer_profile(request, pk):
    developer = get_object_or_404(Developer_Profile, pk=pk)
    name = developer.name
    developer.delete()
    messages.success(request, f'Developer profile for {name} deleted successfully!')
    return HttpResponseRedirect(reverse('admin_dashboard') + '#developers')


# Tech Stack Management
@staff_member_required
def add_tech_stack(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        Teck_Stack.objects.create(title=title)
        messages.success(request, f'Technology "{title}" added successfully!')
        return HttpResponseRedirect(reverse('admin_dashboard') + '#tech-stack')
    
    return render(request, 'admin_dashboard/add_tech_stack.html')


@staff_member_required
def edit_tech_stack(request, pk):
    tech = get_object_or_404(Teck_Stack, pk=pk)
    
    if request.method == 'POST':
        tech.title = request.POST.get('title')
        tech.save()
        messages.success(request, f'Technology updated to "{tech.title}"!')
        return HttpResponseRedirect(reverse('admin_dashboard') + '#tech-stack')
    
    context = {'tech': tech}
    return render(request, 'admin_dashboard/edit_tech_stack.html', context)


@staff_member_required
def delete_tech_stack(request, pk):
    tech = get_object_or_404(Teck_Stack, pk=pk)
    title = tech.title
    tech.delete()
    messages.success(request, f'Technology "{title}" deleted successfully!')
    return HttpResponseRedirect(reverse('admin_dashboard') + '#tech-stack')