from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="home"),
    path("signup/", views.signup, name="signup"),
    path("signup/success/", views.signup_success, name="signup_success"),
    path("process-emails/", views.process_emails, name="process_emails"),
    path("privacy/", views.privacy, name="privacy"),
    path("terms/", views.terms, name="terms"),
]


