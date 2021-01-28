from django.conf.urls.static import static
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path

from HMS import settings
from . import views

app_name = 'accounts'

urlpatterns = [
    path('', views.WelcomeView.as_view()),
    path('register/', views.SignUpView.as_view(), name='register'),
    path('login/', LoginView.as_view(template_name='signup/login.html'), name='login'),
    path('confirm/<str:uid>/<str:token>/<int:check>/', views.ConfirmEmail.as_view(), name='confirm_email'),
    path('activate/<str:uid>/<str:token>/', views.Activate.as_view(), name='activate'),
    path('logout/', LogoutView.as_view(template_name='signup/logout.html'), name='logout')
    ]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
