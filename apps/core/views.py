from django.contrib.auth.models import User, Permission
from django.core.mail import send_mail
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from apps.core.forms import RegistrationForm, LoginForm
from apps.core.models import PortfolioItem
from apps.blog.models import Post
from apps.shop.models import Product
from .utils import send_activation_email
from django.utils.http import urlsafe_base64_decode
from django.utils.encoding import force_str
from django.contrib.auth.tokens import default_token_generator

def home(request):
    portfolio_items = PortfolioItem.objects.all()
    latest_posts = Post.objects.order_by('-created_at')[:3]
    return render(request, "home.html", {
        'portfolio_items': portfolio_items, 
        'latest_posts': latest_posts,
    })


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
# def signup(request):
#     if request.user.is_authenticated:
#         return redirect('homepage')
#     if request.method == 'POST':
#         # Get form data
#         first_name = request.POST.get('first_name')
#         last_name = request.POST.get('last_name')
#         username = request.POST.get('username')
#         email = request.POST.get('email')
#         password = request.POST.get('password')
#         password2 = request.POST.get('password2')
#         # Validation
#         if password != password2:
#             messages.error(request, "Passwords do not match")
#             return redirect('signup')
#         if User.objects.filter(username=username).exists():
#             messages.error(request, "Username already exists")
#             return redirect('signup')
#         if User.objects.filter(email=email).exists():
#             messages.error(request, "Email already registered")
#             return redirect('signup')
#         user = User.objects.create_user(
#             username=username,
#             email=email,
#             password=password,
#             first_name=first_name,
#             last_name=last_name,
#             is_active=False
#         )
#         user.save()
#         user.set_password(form.cleaned_data['password'])
#         user.is_active = False
#         send_activation_email(request, user)
#         messages.success(request, "Registration successful! Please check your email to activate your account.")
#         return redirect('signin')
#     return render(request, 'accounts/register.html')

def signup(request):
    if request.user.is_authenticated:
        return redirect('homepage')

    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            print(form.cleaned_data)
            user = form.save(commit=False)
            # Hash the password properly
            user.set_password(form.cleaned_data['password'])
            user.is_active = False  # account inactive until email activation
            user.save()

            send_activation_email(request, user)
            messages.success(request, "Registration successful! Please check your email to activate your account.")
            return redirect('signin')
    else:
        form = RegistrationForm()

    return render(request, 'accounts/register.html', {'form': form})

def activate(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user)
        messages.success(request, 'Your account has been activated successfully!')
        return redirect('homepage')
    else:
        messages.error(request, 'Activation link is invalid!')
        return redirect('homepage')

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

def custom_404(request, exception):
    return render(request, '404.html', status=404)

def custom_500(request):
    return render(request, '500.html', status=500)

def custom_403(request, exception):
    return render(request, '403.html', status=403)
