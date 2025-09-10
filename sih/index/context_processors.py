from typing import Optional
from django.http import HttpRequest
from .models import Profile


def user_profile(request: HttpRequest) -> dict:
    if not getattr(request, "user", None) or not request.user.is_authenticated:
        return {"user_profile": None}
    profile: Optional[Profile] = None
    try:
        profile = Profile.objects.select_related("user").filter(user=request.user).first()
    except Exception:
        profile = None
    return {"user_profile": profile}


