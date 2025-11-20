from django.contrib.sitemaps import Sitemap
from django.urls import reverse
from .models import CrProfile, Review, University, Department

class CRSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.9

    def items(self):
        # Shudhu Present CRs nibo, deleted_at null thakte hobe
        return CrProfile.objects.filter(
            cr_status='Present',
            deleted_at__isnull=True
        ).select_related('university', 'department').order_by('-created_at')

    def lastmod(self, obj):
        return obj.updated_at

    def location(self, obj):
        # Tomar actual URL name: 'cr_profile'
        return reverse('cr_profile', kwargs={'slug': obj.slug})


class ReviewSitemap(Sitemap):
    changefreq = "daily"
    priority = 0.7

    def items(self):
        # Shudhu approved reviews
        return Review.objects.filter(
            is_approved=True,
            deleted_at__isnull=True
        ).select_related('cr_profile', 'user').order_by('-created_at')

    def lastmod(self, obj):
        return obj.updated_at

    def location(self, obj):
        # Review er CR profile page e niye jabe
        return reverse('cr_profile', kwargs={'slug': obj.cr_profile.slug})


class UniversitySitemap(Sitemap):
    changefreq = "monthly"
    priority = 0.6

    def items(self):
        return University.objects.filter(
            deleted_at__isnull=True  # typo ache tomar model e: daleted_at
        ).order_by('title')

    def lastmod(self, obj):
        return obj.updated_at

    def location(self, obj):
        # University filter page
        return f"/?university={obj.id}"


class DepartmentSitemap(Sitemap):
    changefreq = "monthly"
    priority = 0.6

    def items(self):
        return Department.objects.filter(
            deleted_at__isnull=True  # typo ache tomar model e
        ).order_by('title')

    def lastmod(self, obj):
        return obj.updated_at

    def location(self, obj):
        # Department filter page
        return f"/?department={obj.id}"


class StaticViewSitemap(Sitemap):
    priority = 1.0
    changefreq = 'daily'

    def items(self):
        return ['home', 'all_cr', 'latest_reviews']

    def location(self, item):
        return reverse(item)