
from django.core.exceptions import ValidationError
from django.contrib import messages
from userprofile.models import User
from django.urls import reverse
import logging

logger = logging.getLogger(__name__)


def create_user(strategy, details, backend, user=None, *args, **kwargs):
    """
    Custom pipeline function to create user with Google OAuth
    """
    if user:
        return {'is_new': False}
    
    # Extract user information from Google
    email = details.get('email')
    first_name = details.get('first_name', '')
    last_name = details.get('last_name', '')
    
    if not email:
        logger.error("Email not provided by Google OAuth")
        return None
    
    # Check if user already exists
    existing_user = User.objects.filter(email=email).first()
    if existing_user:
        # Update existing user info if needed
        if not existing_user.is_email_verified:
            existing_user.is_email_verified = True
            existing_user.is_active = True
            existing_user.save()
        return {
            'is_new': False,
            'user': existing_user
        }
    
    try:
        # Create new user with Google OAuth
        user = User.objects.create_user(
            email=email,
            first_name=first_name or 'User',
            last_name=last_name or '',
            password=None, 
            is_email_verified=True,  
            is_active=True,
        )
        
      
        user.student_id = f"GOOGLE_{user.id}"
        user.save()
        
        logger.info(f"New user created via Google OAuth: {email}")
        
        return {
            'is_new': True,
            'user': user
        }
        
    except Exception as e:
        logger.error(f"Error creating user via Google OAuth: {str(e)}")
        return None


def send_validation_email(strategy, backend, code):
    """
    Send email validation if needed
    """
    pass


def user_details(strategy, details, user=None, *args, **kwargs):
    """
    Update user details from social auth
    """
    if not user:
        return
    
    changed = False
    
    # Update first name if empty
    if not user.first_name and details.get('first_name'):
        user.first_name = details['first_name']
        changed = True
    
    # Update last name if empty
    if not user.last_name and details.get('last_name'):
        user.last_name = details['last_name']
        changed = True
    
    # Update profile picture from Google if not set
    if not user.profile_picture and details.get('picture'):
        user.profile_picture = details['picture']
        changed = True
    
    if changed:
        user.save()
    
    return {'user': user}



def get_dashboard_url(backend, user, *args, **kwargs):
 
    if user and hasattr(user, 'slug') and user.slug:
        # Use the reverse function to build the URL with the slug parameter
        return reverse('user_dashboard', kwargs={'slug': user.slug})
    
    # Fallback to a safe URL if the user or slug is missing
    return reverse('home') # Or another safe page