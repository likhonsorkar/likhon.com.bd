from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm
from django.core.exceptions import ValidationError
from apps.blog.models import Comment
# -----------------------------
# Registration Form
# -----------------------------
class RegistrationForm(forms.ModelForm):
    first_name = forms.CharField(max_length=30, required=True, widget=forms.TextInput(
        attrs={'placeholder': 'First Name', 'class': 'w-full px-4 py-3 border rounded-lg focus:ring-2 focus:ring-purple-mountain-majesty'}
    ))
    last_name = forms.CharField(max_length=30, required=True, widget=forms.TextInput(
        attrs={'placeholder': 'Last Name', 'class': 'w-full px-4 py-3 border rounded-lg focus:ring-2 focus:ring-purple-mountain-majesty'}
    ))
    email = forms.EmailField(required=True, widget=forms.EmailInput(
        attrs={'placeholder': 'Email', 'class': 'w-full px-4 py-3 border rounded-lg focus:ring-2 focus:ring-purple-mountain-majesty'}
    ))
    password = forms.CharField(required=True, widget=forms.PasswordInput(
        attrs={'placeholder': 'Password', 'class': 'w-full px-4 py-3 border rounded-lg focus:ring-2 focus:ring-purple-mountain-majesty'}
    ))
    password2 = forms.CharField(required=True, widget=forms.PasswordInput(
        attrs={'placeholder': 'Confirm Password', 'class': 'w-full px-4 py-3 border rounded-lg focus:ring-2 focus:ring-purple-mountain-majesty'}
    ))

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'username', 'password']

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if User.objects.filter(username=username).exists():
            raise ValidationError("Username already exists")
        return username

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise ValidationError("Email already exists")
        return email

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        password2 = cleaned_data.get("password2")
        if password and password2 and password != password2:
            raise ValidationError("Passwords do not match")
        return cleaned_data


# -----------------------------
# Login Form
# -----------------------------
class LoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(
        attrs={'placeholder': 'Username or Email', 'class': 'w-full px-4 py-3 border rounded-lg focus:ring-2 focus:ring-purple-mountain-majesty'}
    ))
    password = forms.CharField(widget=forms.PasswordInput(
        attrs={'placeholder': 'Password', 'class': 'w-full px-4 py-3 border rounded-lg focus:ring-2 focus:ring-purple-mountain-majesty'}
    ))
