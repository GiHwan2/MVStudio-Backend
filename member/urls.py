# member/urls.py

from django.urls import path
from .views import MemberSignUpView,MemberDetailView, MemberLoginView



urlpatterns = [
    path('', MemberSignUpView.as_view(), name='member-sign-up'),
    path('<int:member_id>/',MemberDetailView.as_view(), name='member-detail'),
    path('login/', MemberLoginView.as_view(), name='member-login'),
]