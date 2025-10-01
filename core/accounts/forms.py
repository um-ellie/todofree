from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from .models import Profile

User = get_user_model()

class SignUpForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('email',)


class ProfileForm(forms.ModelForm):
    # Add a checkbox to remove the profile image
    remove_image = forms.BooleanField(
        required=False,
        label="Remove current image"
    )

    class Meta:
        model = Profile
        fields = ['first_name', 'last_name', 'bio', 'image', 'date_of_birth', 'location', 'language', 'timezone', 'social_links']
        widgets = {
            'first_name': forms.TextInput(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded focus:outline-none focus:ring-2 focus:ring-indigo-400'
            }),
            'last_name': forms.TextInput(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded focus:outline-none focus:ring-2 focus:ring-indigo-400'
            }),
            'bio': forms.Textarea(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded focus:outline-none focus:ring-2 focus:ring-indigo-400'
            }),
            'image': forms.ClearableFileInput(attrs={
                'class': 'w-full'
            }),
            'date_of_birth': forms.DateInput(attrs={
                'type': 'date',
                'class': 'w-full px-4 py-2 border border-gray-300 rounded focus:outline-none focus:ring-2 focus:ring-indigo-400'
            }),
            'location': forms.TextInput(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded focus:outline-none focus:ring-2 focus:ring-indigo-400'
            }),
            'language': forms.TextInput(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded focus:outline-none focus:ring-2 focus:ring-indigo-400'
            }),
            'timezone': forms.TextInput(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded focus:outline-none focus:ring-2 focus:ring-indigo-400'
            }),
            'social_links': forms.Textarea(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded focus:outline-none focus:ring-2 focus:ring-indigo-400'
            }),
        }

    def save(self, commit=True):
        profile = super().save(commit=False)
        # If the remove_image checkbox is checked, delete the current image
        if self.cleaned_data.get('remove_image') and profile.image:
            profile.image.delete(save=False)
            profile.image = None
        if commit:
            profile.save()
        return profile
