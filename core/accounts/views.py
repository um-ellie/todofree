from django.urls import reverse_lazy
from django.contrib.auth import get_user_model
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import CreateView, DetailView, UpdateView

from .forms import SignUpForm, ProfileForm
from .models import Profile


User = get_user_model()


class SignUpView(CreateView):
    """User registration view"""
    form_class = SignUpForm
    template_name = "registration/sign_up.html"
    success_url = reverse_lazy("accounts:login")


class CustomLoginView(LoginView):
    """Login with custom template"""
    template_name = "registration/login.html"

    def get_success_url(self):
        return reverse_lazy("accounts:profile") # Redirect to profile after login


class CustomLogoutView(LoginRequiredMixin, LogoutView):
    """Logout and redirect to login page"""
    next_page = reverse_lazy("accounts:login")



class ProfileDetailView(LoginRequiredMixin, DetailView):
    """Show current user's profile"""
    model = Profile
    context_object_name = "profile"
    template_name = "registration/profile.html"

    def get_object(self, queryset=None):
        return self.request.user.profile


class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    """Edit current user's profile"""
    model = Profile
    form_class = ProfileForm
    template_name = "registration/edit_profile.html"
    success_url = reverse_lazy("accounts:profile")

    def get_object(self, queryset=None):
        return self.request.user.profile
