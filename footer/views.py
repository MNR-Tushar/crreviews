from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json

from .models import *

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
    context = {
        'page_title': 'Developer - CR Reviews'
    }
    return render(request, 'footer_page/developer.html', context)

# Contact Message Handler
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
                return JsonResponse({
                    'success': False, 
                    'error': 'Email and message are required'
                })
            
            # Validate email format (basic check)
            if '@' not in email or '.' not in email:
                return JsonResponse({
                    'success': False, 
                    'error': 'Please provide a valid email address'
                })
            
            # Validate message length
            if len(message.strip()) < 10:
                return JsonResponse({
                    'success': False, 
                    'error': 'Message must be at least 10 characters long'
                })
            
            if len(message) > 1000:
                return JsonResponse({
                    'success': False, 
                    'error': 'Message is too long (max 1000 characters)'
                })
            
            # Create contact message
            contact = ContactMessage.objects.create(
                name=name,
                email=email,
                message=message
            )
            
            return JsonResponse({
                'success': True, 
                'message': 'Thank you! Your message has been sent successfully. We\'ll get back to you soon.'
            })
            
        except Exception as e:
            return JsonResponse({
                'success': False, 
                'error': f'An error occurred: {str(e)}'
            })
    
    return JsonResponse({
        'success': False, 
        'error': 'Invalid request method'
    })