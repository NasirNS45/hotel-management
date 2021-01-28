"""
Definition of urls for HotelFlexProject.
"""

# Uncomment the next lines to enable the admin:
from django.urls import path, include
from django.contrib import admin, admindocs

admin.autodiscover()

urlpatterns = [
    path('', include('app.urls')),
    path('accounts/', include('signup.urls')),
    path('admin_panel/', include('admin.urls')),
    path('admin/', admin.site.urls, name='admin')
]
