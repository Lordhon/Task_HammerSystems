
from django.contrib import admin
from django.urls import path

from User.views import SendCode, VerifyCode, Profile, ActivateCode

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/send_code/', SendCode.as_view()),
    path('api/verify_code/', VerifyCode.as_view()),
    path('api/profile/', Profile.as_view()),
    path('api/activate-invite/', ActivateCode.as_view()),

]
