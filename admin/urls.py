from django.urls import path
from . import views

urlpatterns = [
    path('adminh4u/', views.adminh4u, name='adminh4u'),
    path('adminlogin/', views.AdminLoginView.as_view(), name='adminlogin'),
    path('adminbooking/', views.adminbooking, name='adminbooking'),
    path('salesanalysis/', views.salesanalysis, name='salesanalysis')
]
