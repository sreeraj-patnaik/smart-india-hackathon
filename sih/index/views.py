from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.models import User
from .models import Profile
from django.contrib.auth.decorators import login_required
from django.utils.crypto import get_random_string
from .models import TestReport, ChatMessage, ForumPost, DoctorContact

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


def _get_privacy_flags(request):
    is_anon = bool(request.session.get("privacy_is_anon", False))
    anon_id = request.session.get("privacy_anon_id")
    if is_anon and not anon_id:
        anon_id = get_random_string(16)
        request.session["privacy_anon_id"] = anon_id
    return is_anon, anon_id


@login_required
def dashboard(request):
    is_anon, anon_id = _get_privacy_flags(request)
    reports = TestReport.objects.filter(user=request.user).order_by("-created_at")[:10]
    posts = ForumPost.objects.filter(user=request.user).order_by("-created_at")[:5]
    chats = ChatMessage.objects.filter(user=request.user).order_by("-created_at")[:10]
    doctors = DoctorContact.objects.all()[:12]
    return render(request, "dashboard.html", {
        "is_anon": is_anon,
        "anon_id": anon_id,
        "reports": reports,
        "posts": posts,
        "chats": chats,
        "doctors": doctors,
    })


@login_required
def toggle_privacy(request):
    if request.method == "POST":
        current = bool(request.session.get("privacy_is_anon", False))
        request.session["privacy_is_anon"] = not current
        if not current and not request.session.get("privacy_anon_id"):
            request.session["privacy_anon_id"] = get_random_string(16)
        messages.info(request, f"Privacy set to {'Anonymous' if not current else 'Public'}.")
    return redirect("dashboard")


@login_required
def phq9(request):
    is_anon, anon_id = _get_privacy_flags(request)
    if request.method == "POST":
        answers = {f"q{i}": int(request.POST.get(f"q{i}", 0)) for i in range(1, 10)}
        score = sum(answers.values())
        TestReport.objects.create(
            user=request.user, test_type="PHQ9", score=score,
            raw_answers=answers, is_anonymous=is_anon, anon_id=anon_id or ""
        )
        messages.success(request, f"PHQ-9 submitted. Score: {score}")
        return redirect("dashboard")
    return render(request, "tests/phq9.html")


@login_required
def gad7(request):
    is_anon, anon_id = _get_privacy_flags(request)
    if request.method == "POST":
        answers = {f"q{i}": int(request.POST.get(f"q{i}", 0)) for i in range(1, 8)}
        score = sum(answers.values())
        TestReport.objects.create(
            user=request.user, test_type="GAD7", score=score,
            raw_answers=answers, is_anonymous=is_anon, anon_id=anon_id or ""
        )
        messages.success(request, f"GAD-7 submitted. Score: {score}")
        return redirect("dashboard")
    return render(request, "tests/gad7.html")


@login_required
def chat(request):
    is_anon, anon_id = _get_privacy_flags(request)
    if request.method == "POST":
        text = request.POST.get("message", "").strip()
        if text:
            ChatMessage.objects.create(
                user=request.user, message=text, is_user=True,
                is_anonymous=is_anon, anon_id=anon_id or ""
            )
            # Simple AI echo/placeholder
            ChatMessage.objects.create(
                user=request.user, message="Thanks for sharing. I'm here to help.", is_user=False,
                is_anonymous=is_anon, anon_id=anon_id or ""
            )
        return redirect("dashboard")
    return redirect("dashboard")


@login_required
def forum(request):
    is_anon, anon_id = _get_privacy_flags(request)
    if request.method == "POST":
        title = request.POST.get("title", "").strip()
        content = request.POST.get("content", "").strip()
        if title and content:
            ForumPost.objects.create(
                user=request.user, title=title, content=content,
                is_anonymous=is_anon, anon_id=anon_id or ""
            )
            messages.success(request, "Posted to forum.")
        return redirect("dashboard")
    return redirect("dashboard")


@login_required
def doctors(request):
    doctors = DoctorContact.objects.all()
    return render(request, "doctors.html", {"doctors": doctors})