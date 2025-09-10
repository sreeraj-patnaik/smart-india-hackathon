from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.models import User
from .models import Profile

# Create your views here.
def home(request):
    return render(request, "hi.html")
def about(request):
    return render(request, "about.html")
def login(request):
    if request.method == "POST":
        username = request.POST.get("username", "").strip()
        password = request.POST.get("password", "")

        user = authenticate(request, username=username, password=password)
        if user is not None:
            auth_login(request, user)
            messages.success(request, "Logged in successfully.")
            return redirect("home")
        else:
            messages.error(request, "Invalid credentials. Please try again.")

    return render(request, "login.html")
def signup(request):
    if request.method == "POST":
        fullname = request.POST.get("fullname", "").strip()
        username = request.POST.get("username", "").strip()
        email = request.POST.get("email", "").strip()
        password1 = request.POST.get("password1", "")
        password2 = request.POST.get("password2", "")
        dob = request.POST.get("dob")
        gender = request.POST.get("gender", "")
        college_name = request.POST.get("college_name", "").strip()
        college_type = request.POST.get("college_type", "").strip()
        college_pin = request.POST.get("college_pin", "").strip()
        city = request.POST.get("city", "").strip()
        state = request.POST.get("state", "").strip()
        country = request.POST.get("country", "").strip()
        health_conditions = request.POST.get("health_conditions", "").strip()
        photo = request.FILES.get("photo")

        if not username or not password1 or not password2:
            messages.error(request, "Please fill out all required fields.")
            return render(request, "signup.html")

        if password1 != password2:
            messages.error(request, "Passwords do not match.")
            return render(request, "signup.html")

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already taken.")
            return render(request, "signup.html")

        if email and User.objects.filter(email=email).exists():
            messages.error(request, "Email already in use.")
            return render(request, "signup.html")

        try:
            first_name = fullname
            user = User.objects.create_user(
                username=username,
                email=email,
                password=password1,
                first_name=first_name,
            )
            profile = Profile.objects.create(
                user=user,
                full_name=fullname,
                dob=dob or None,
                gender=gender,
                college_name=college_name,
                college_type=college_type,
                college_pin=college_pin,
                city=city,
                state=state,
                country=country,
                health_conditions=health_conditions,
            )
            if photo:
                profile.photo = photo
                profile.save()
            auth_login(request, user)
            messages.success(request, "Account created successfully.")
            return redirect("home")
        except Exception as exc:
            messages.error(request, "Could not create account. Please try again.")

    return render(request, "signup.html")
def logout(request):
    if request.method == "POST" or request.method == "GET":
        auth_logout(request)
        messages.info(request, "You have been logged out.")
    return redirect("home")