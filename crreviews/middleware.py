from admin_dashboard.models import VisitorLog
from user_agents import parse

class VisitorTrackingMiddleware:
    IGNORED_USER_AGENTS = (
        'uptimerobot',
    )
    IGNORED_PATHS = (
        '/robots.txt',
        '/sitemap.xml',
    )

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if self.should_ignore_path(request.path):
            return self.get_response(request)

        # Get user agent
        user_agent = request.META.get('HTTP_USER_AGENT', '')

        if self.should_ignore_user_agent(user_agent):
            return self.get_response(request)

        # Get IP address
        ip_address = self.get_client_ip(request)
        
        # Parse user agent for device info
        user_agent_parsed = parse(user_agent)
        device_type = 'Mobile' if user_agent_parsed.is_mobile else 'Tablet' if user_agent_parsed.is_tablet else 'Desktop'
        browser = f"{user_agent_parsed.browser.family} {user_agent_parsed.browser.version_string}"
        
        # Get user if authenticated
        user = request.user if request.user.is_authenticated else None
        
        # Save visitor log
        try:
            VisitorLog.objects.create(
                ip_address=ip_address,
                user_agent=user_agent,
                path=request.path,
                method=request.method,
                user=user,
                device_type=device_type,
                browser=browser
            )
        except Exception as e:
            print(f"Error logging visitor: {e}")
        
        response = self.get_response(request)
        return response

    def should_ignore_user_agent(self, user_agent):
        """Skip uptime checks and other configured synthetic traffic."""
        normalized_user_agent = user_agent.lower()
        return any(agent in normalized_user_agent for agent in self.IGNORED_USER_AGENTS)

    def should_ignore_path(self, path):
        """Skip site metadata endpoints from visitor analytics."""
        normalized_path = path.rstrip('/') or '/'
        return normalized_path in self.IGNORED_PATHS
    
    def get_client_ip(self, request):
        """Get the client's IP address from the request"""
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip
