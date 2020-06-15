
from django.urls import path
from .views import signup_view,login_view,onboarding
app_name = "user"
urlpatterns = [
    path('signup/',signup_view,name = "signup"),
    path('login/',login_view,name = "login"),
    path('activate/<uidb64>/<token>/', onboarding, name="activate"),
    # path('onboard/<str:regno>',onboarding,name = "onboard"),
]