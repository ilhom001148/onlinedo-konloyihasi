from django.urls import path
from . import views
from .views import HomeView

urlpatterns=[
    path('', HomeView.as_view(), name='index'),
    path('register/',views.RegisterView.as_view(),name='register'),
    path('login/',views.LoginView.as_view(),name='login'),
    path('logout/',views.logout_,name='logout'),
    path('verify_email/', views.Verify_EmailView.as_view(), name='verify_email'),
    path('resend-code/', views.ResendCodeView.as_view(), name='resend_code'),
]