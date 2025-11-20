
from django.contrib import admin
from django.http import HttpResponse
from django.urls import include, path
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.sitemaps.views import sitemap
from django.views.generic import TemplateView

from cr.sitemaps import (
    CRSitemap, 
    ReviewSitemap, 
    UniversitySitemap, 
    DepartmentSitemap, 
    StaticViewSitemap
)

sitemaps = {
    'crs': CRSitemap,
    'reviews': ReviewSitemap,
    'universities': UniversitySitemap,
    'departments': DepartmentSitemap,
    'static': StaticViewSitemap,
}
# Robots.txt view function
def robots_txt(request):
    lines = [
        "User-agent: *",
        "Allow: /",
        "Disallow: /admin/",
        "Disallow: /settings/",
        "Disallow: /edit_cr/",
        "Disallow: /delete_cr/",
        "Disallow: /submit_review/",
        "Disallow: /edit_review/",
        "Disallow: /delete_review/",
        "",
        "Sitemap: https://crreviews.onrender.com/sitemap.xml",
    ]
    return HttpResponse("\n".join(lines), content_type="text/plain")

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',include('cr.urls')),
    path('',include('userprofile.urls')),
    path('',include('footer.urls')),
    path('',include('admin_dashboard.urls')),
    path('auth/', include('social_django.urls', namespace='social')),

    # Sitemap
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps}, 
         name='django.contrib.sitemaps.views.sitemap'),
    
    # Robots.txt
    path('robots.txt', robots_txt),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

