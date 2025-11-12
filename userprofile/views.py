import cloudinary
from django.contrib import messages
from django.forms import ValidationError
from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth import authenticate,login as auth_login,logout as auth_logout
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from cr.models import *
from .models import *
from django.contrib.auth.decorators import login_required
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.password_validation import validate_password
from django.core.mail import send_mail,EmailMessage
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.conf import settings
from django.utils import timezone
import logging
import uuid
from django.contrib.admin.views.decorators import staff_member_required


logger = logging.getLogger(__name__)

def send_verification_email(user, request):
    """Send email verification link to user"""
    try:
        verification_url = request.build_absolute_uri(
            f'/verify-email/{user.email_verification_token}/'
        )
        
        subject = 'Verify Your Email - CR Review'
        
        # HTML email template
        html_message = render_to_string('user_profile/emails/verification_email.html', {
            'user': user,
            'verification_url': verification_url,
        })
        plain_message = strip_tags(html_message)
        
        # Send email with timeout handling
        from django.core.mail import EmailMultiAlternatives
        
        email = EmailMultiAlternatives(
            subject=subject,
            body=plain_message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=[user.email]
        )
        email.attach_alternative(html_message, "text/html")
        email.send(fail_silently=False)
        
        logger.info(f"Verification email sent successfully to {user.email}")
        return True
        
    except Exception as e:
        logger.error(f"Error sending verification email to {user.email}: {str(e)}")
        return False


def send_password_reset_email(user, request):
    """Send password reset link to user"""
    try:
        reset_url = request.build_absolute_uri(
            f'/reset-password/{user.password_reset_token}/'
        )
        
        subject = 'Reset Your Password - CR Review'
        
        # HTML email template
        html_message = render_to_string('user_profile/emails/password_reset_email.html', {
            'user': user,
            'reset_url': reset_url,
        })
        plain_message = strip_tags(html_message)
        
        # Send email
        from django.core.mail import EmailMultiAlternatives
        
        email = EmailMultiAlternatives(
            subject=subject,
            body=plain_message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=[user.email]
        )
        email.attach_alternative(html_message, "text/html")
        email.send(fail_silently=False)
        
        logger.info(f"Password reset email sent successfully to {user.email}")
        return True
        
    except Exception as e:
        logger.error(f"Error sending password reset email to {user.email}: {str(e)}")
        return False

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
        
        if len(password) < 8:
            messages.error(request, 'Password must be at least 8 characters long!')
            return redirect('registration')
        
        if password.isdigit():
            messages.error(request, 'Password must contain at least one letter!')
            return redirect('registration')
        
        try:
            validate_password(password)
        except ValidationError as e:
            messages.error(request, str(e))
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

            try:
                email_sent = send_verification_email(user, request)
                if email_sent:
                    messages.success(request, 'Registration successful! Please check your email to verify your account.')
                else:
                    messages.warning(request, 'Account created but verification email failed. Please use "Resend Verification" option.')
            except Exception as e:
                logger.error(f"Email sending failed during registration: {str(e)}")
                messages.warning(request, 'Account created but email could not be sent. Please use "Resend Verification" option.')
            
            return redirect('verification_pending')
            
        except Exception as e:
            logger.error(f"Registration error: {str(e)}")
            messages.error(request, f'Registration failed: {str(e)}')
            return redirect('registration')
    
    
    universitys = University.objects.all().order_by('title')
    departments = Department.objects.all().order_by('title')
    
    context = {
        'universitys': universitys,
        'departments': departments,
    }
    
    return render(request, 'user_profile/registration.html', context)


def verify_email(request, token):
    
    try:
        user = User.objects.get(email_verification_token=token)
        
        if user.is_email_verified:
            messages.info(request, 'Your email is already verified. Please login.')
            return redirect('login')
        
        if not user.is_email_verification_token_valid():
            messages.error(request, 'Verification link has expired. Please request a new one.')
            return redirect('resend_verification')
        
        user.is_email_verified = True
        user.is_active = True
        user.save()
        
        messages.success(request, 'Email verified successfully! You can now login.')
        return redirect('login')
        
    except User.DoesNotExist:
        messages.error(request, 'Invalid verification link.')
        return redirect('login')


def verification_pending(request):
    
    return render(request, 'user_profile/verification_pending.html')


def resend_verification_email(request):
  
    if request.method == 'POST':
        email = request.POST.get('email')
        
        try:
            user = User.objects.get(email=email)
            
            if user.is_email_verified:
                messages.info(request, 'Your email is already verified. Please login.')
                return redirect('login')
            
            # Generate new token
            user.email_verification_token = uuid.uuid4()
            user.email_verification_token_created = timezone.now()
            user.save()
            
            if send_verification_email(user, request):
                messages.success(request, 'Verification email sent! Please check your inbox.')
            else:
                messages.error(request, 'Failed to send email. Please try again later.')
                
        except User.DoesNotExist:
            messages.error(request, 'No account found with this email.')
        
        return redirect('resend_verification')
    
    return render(request, 'user_profile/resend_verification.html')

def login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        
        try:
            user = User.objects.get(email=email)
            
            if not user.is_email_verified:
                messages.warning(request, 'Please verify your email first. Check your inbox.')
                return redirect('verification_pending')
            
        except User.DoesNotExist:
            messages.error(request, 'Invalid email or password!')
            return redirect('login')
        
        user = authenticate(request, email=email, password=password)
        
        if user is not None:
            auth_login(request, user)
            messages.success(request, 'Successfully logged in!')
            return redirect('home')
        else:
            messages.error(request, 'Invalid email or password!')
            return redirect('login')
    
    return render(request, 'user_profile/login.html')



def forgot_password(request):
    
    if request.method == 'POST':
        email = request.POST.get('email')
        
        try:
            user = User.objects.get(email=email)
            
            if not user.is_email_verified:
                messages.error(request, 'Please verify your email first.')
                return redirect('resend_verification')
            
            # Generate password reset token
            user.generate_password_reset_token()
            
            if send_password_reset_email(user, request):
                messages.success(request, 'Password reset link sent to your email!')
                return redirect('password_reset_done')
            else:
                messages.error(request, 'Failed to send email. Please try again.')
                
        except User.DoesNotExist:
            # Don't reveal if email exists
            messages.success(request, 'If this email exists, you will receive a password reset link.')
            return redirect('password_reset_done')
        
        return redirect('forgot_password')
    
    return render(request, 'user_profile/forgot_password.html')


def reset_password(request, token):
    
    try:
        user = User.objects.get(password_reset_token=token)
        
        if not user.is_password_reset_token_valid():
            messages.error(request, 'Password reset link has expired. Please request a new one.')
            return redirect('forgot_password')
        
        if request.method == 'POST':
            new_password = request.POST.get('new_password')
            confirm_password = request.POST.get('confirm_password')
            
            if new_password != confirm_password:
                messages.error(request, 'Passwords do not match!')
                return redirect('reset_password', token=token)
            
            if len(new_password) < 8:
                messages.error(request, 'Password must be at least 8 characters long!')
                return redirect('reset_password', token=token)
            
            if new_password.isdigit():
                messages.error(request, 'Password cannot be entirely numeric!')
                return redirect('reset_password', token=token)
            
            try:
                validate_password(new_password)
            except ValidationError as e:
                messages.error(request, ' '.join(e.messages))
                return redirect('reset_password', token=token)
            
            user.set_password(new_password)
            user.password_reset_token = None
            user.password_reset_token_created = None
            user.save()
            
            messages.success(request, 'Password reset successfully! You can now login.')
            return redirect('login')
        
        return render(request, 'user_profile/reset_password.html', {'token': token})
        
    except User.DoesNotExist:
        messages.error(request, 'Invalid password reset link.')
        return redirect('forgot_password')


def password_reset_done(request):
    
    return render(request, 'user_profile/password_reset_done.html')




@login_required
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
    add_crs = CrProfile.objects.filter(user=request.user)
 
    items_per_page = 3
    add_crs_paginator = Paginator(add_crs, items_per_page)
    add_crs_page = request.GET.get('add_crs_page', 1)
    add_crs = add_crs_paginator.get_page(add_crs_page)

    saved_crs_paginator = Paginator(saved_crs, items_per_page)
    saved_crs_page = request.GET.get('saved_crs_page', 1)
    saved_crs = saved_crs_paginator.get_page(saved_crs_page)

    review_paginator = Paginator(review, items_per_page)
    review_page = request.GET.get('review_page', 1)
    review = review_paginator.get_page(review_page)

    context = {
        'user':user,
        'review':review,
        'last':last,
        'saved_crs':saved_crs,
        'last_cr_saved':last_cr_saved,
        'add_crs':add_crs,
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
def edit_user(request,slug):

    user = get_object_or_404(User,slug=slug)
    university = University.objects.all().order_by('title')
    department = Department.objects.all().order_by('title')

    if request.user != user:
        messages.error(request, "You are not authorized to edit this profile.")
        return redirect('home')
    

    if request.method == 'POST':
            user.first_name = request.POST.get('first_name')
            user.last_name = request.POST.get('last_name')
            user.email = request.POST.get('email')
            user.student_id = request.POST.get('student_id')
            user.batch = request.POST.get('batch')
            user.dept_batch = request.POST.get('dept_batch')
            user.section = request.POST.get('section')
            user.bio = request.POST.get('bio')
            user.gender = request.POST.get('gender')
            user.date_of_birth = request.POST.get('date_of_birth') or None
            new_picture = request.FILES.get('profile_picture')
            if new_picture:
                try:
                    # Delete old picture from Cloudinary if exists
                    if user.profile_picture and 'cloudinary' in user.profile_picture:
                        public_id = user.profile_picture.split('/')[-1].split('.')[0]
                        try:
                            cloudinary.uploader.destroy(f'users/user_{user.id}/profile_pictures/{public_id}')
                        except:
                            pass
                    
                    # Upload new picture
                    upload_result = cloudinary.uploader.upload(
                        new_picture,
                        folder=f'users/user_{user.id}/profile_pictures',
                        public_id=f'profile_{user.id}',
                        overwrite=True,
                        transformation=[
                            {'width': 500, 'height': 500, 'crop': 'fill', 'gravity': 'face'},
                            {'quality': 'auto:good'},
                            {'fetch_format': 'auto'}
                        ]
                    )
                    
                    # Save only the secure URL (not as ImageField)
                    user.profile_picture = upload_result['secure_url']
                    
                except Exception as e:
                    messages.error(request, f'Failed to upload image: {str(e)}')

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

@login_required
def user_settings(request):

    return render(request,'user_profile/settings.html')

@login_required
def change_password(request):
    if request.method == 'POST':
        current_password = request.POST.get('current_password')
        new_password = request.POST.get('new_password')
        confirm_password = request.POST.get('confirm_password')

        if not request.user.check_password(current_password):
            messages.error(request, 'Current password is incorrect!')
            return redirect('change_password')

        if new_password != confirm_password:
            messages.error(request, 'New password and confirm password do not match!')
            return redirect('change_password')

        if len(new_password) < 8:
            messages.error(request, 'Password must be at least 8 characters long!')
            return redirect('change_password')
        
        if new_password.isdigit():
            messages.error(request, 'Password cannot be entirely numeric!')
            return redirect('change_password')

        try:
            validate_password(new_password)
        except ValidationError as e:
            messages.error(request, ' '.join(e.messages))
            return redirect('change_password')

        request.user.set_password(new_password)
        request.user.save()
        update_session_auth_hash(request, request.user)
        messages.success(request, 'Password changed successfully!')
        return redirect('settings')

    return render(request,'user_profile/change_password.html')


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


