from django.contrib import admin

# Register your models here.

from .models import Profile
admin.site.register(Profile)

from .models import DoctorContact
admin.site.register(DoctorContact)

from .models import TestReport
admin.site.register(TestReport)

from .models import ChatMessage
admin.site.register(ChatMessage)

from .models import ForumPost
admin.site.register(ForumPost)
