
from django.contrib import messages
from django.shortcuts import redirect, render
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from .models import *
from userprofile.models import *
from admin_dashboard.models import *

# About Us Page
def about_us(request):
    
    return render(request, 'footer_page/about_us.html')

# Privacy Policy Page
def privacy_policy(request):
    context = {
        'page_title': 'Privacy Policy - CR Reviews'
    }
    return render(request, 'footer_page/privacy_policy.html', context)

# Terms & Conditions Page
def terms_conditions(request):
    context = {
        'page_title': 'Terms & Conditions - CR Reviews'
    }
    return render(request, 'footer_page/terms_conditions.html', context)

# Help & Support Page
def help_support(request):
    context = {
        'page_title': 'Help & Support - CR Reviews'
    }
    return render(request, 'footer_page/help_support.html', context)


# Developer Page
def developer(request):

    
    
    developer_profiles = Developer_Profile.objects.all()



    context = {
        'page_title': 'Developer - CR Reviews',
        'dp': developer_profiles,
    }
    return render(request, 'footer_page/developer.html', context)

# Contact Message Handler
@login_required(login_url='login')
@csrf_exempt
def contact_message(request):
    
    if request.method == 'POST':
        try:
            # Get form data
            name = request.POST.get('name', 'Anonymous')
            email = request.POST.get('email')
            message = request.POST.get('message')

            
            
            # Validate required fields
            if not email or not message:
                messages.error(request, 'Please fill in all required fields.')
                return redirect('home')  
            
            # Validate email format (basic check)
            if '@' not in email or '.' not in email:
                messages.error(request, 'Please enter a valid email address.')
                return redirect('home')
            
            # Validate message length
            if len(message.strip()) < 10:
                messages.error(request, 'Message must be at least 10 characters long.')
                return redirect('home')
            
            if len(message) > 1000:
                messages.error(request, 'Message must be less than 1000 characters long.')
                return redirect('home')
            
            if not User.is_authenticated:
                messages.error(request, 'You must be logged in to send a contact message.')
                return redirect('home')
            
            # Create contact message
            contact = ContactMessage.objects.create(
                name=name,
                email=email,
                message=message
            )
            
            messages.success(request, 'Your message has been sent successfully!')
            return redirect('home')
            
        except Exception as e:
            messages.error(request, 'An error occurred while processing your request.')
            return redirect('home')
    
    messages.error(request, 'Invalid request method.')
    return redirect('home')