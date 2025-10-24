from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json

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

# Contact Message Handler
@csrf_exempt
def contact_message(request):
    if request.method == 'POST':
        try:
            email = request.POST.get('email')
            message = request.POST.get('message')
            
           
            
            return JsonResponse({'success': True, 'message': 'Message sent successfully'})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})
    
    return JsonResponse({'success': False, 'error': 'Invalid request method'})
