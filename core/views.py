from django.contrib.auth.models import User, Permission
from django.core.mail import send_mail
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from core.forms import RegistrationForm, LoginForm


def home(request):
    return render(request, "home.html")


def signin(request):
    if request.user.is_authenticated:
        return redirect('homepage')
    if request.method == "POST":
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f"Welcome back, {user.username}!")
                return redirect('homepage')
            else:
                messages.error(request, "Invalid username or password")
        else:
            messages.error(request, "Invalid username or password")
    else:
        form = LoginForm()
    return render(request, 'accounts/login.html', {'form': form})
def signup(request):
    if request.user.is_authenticated:
        return redirect('homepage')
    if request.method == 'POST':
        # Get form data
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        username = request.POST.get('username')
        email = request.POST.get('email')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        # Validation
        if password1 != password2:
            messages.error(request, "Passwords do not match")
            return redirect('signup')
        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists")
            return redirect('signup')
        if User.objects.filter(email=email).exists():
            messages.error(request, "Email already registered")
            return redirect('signup')
        user = User.objects.create_user(
            username=username,
            email=email,
            password=password1,
            first_name=first_name,
            last_name=last_name
        )
        user.save()
        messages.success(request, "Registration successful! Please login.")
        return redirect('signin')
    return render(request, 'accounts/register.html')
def contact(request):
    if request.method == "POST":
        name = request.POST.get("name")
        email = request.POST.get("email")
        message = request.POST.get("message")
        subject = f"New Contact Form Submission from {name}"
        body = f"""
        You received a new message from Likhon.com.bd:
        Name: {name}
        Email: {email}
        Message:
        {message}
        """
        try:
            send_mail(subject, body, email, ["contact@likhon.com.bd"])
            messages.success(request, "Your message has been sent successfully!")
        except Exception as e:
            messages.error(request, f"Failed to send email: {e}")
        return redirect("contact")
    return render(request, "contact.html")

def working(request):
    return render(request, "working.html")

def accessdenied(request):
    return render(request, "accessdenied.html")

@login_required
def logout_view(request):
    logout(request)
    messages.success(request, "You have successfully logged out.")
    return redirect('signin')
def career(request):
    return render(request, "career.html")