
from django.urls import path
from .views import api_signup_view,api_verify_token,api_onboarding,api_filter_view,api_new_user,verify_cookie_token,api_detail_view
from rest_framework.authtoken import views
app_name = "api"
urlpatterns = [
    path('signup/<str:regno>',api_signup_view,name = "api_signup"),
    path('verify/<uidb64>/<token>/', api_verify_token, name="api_verify_token"),
    path('onboard/',api_onboarding,name = "api_onboard"),
    path('login/',views.obtain_auth_token,name = "api_login"),
    path('cookie/',verify_cookie_token,name = "verify_cookie_token"),
    path('detail/<str:regno>',api_detail_view.as_view(),name = "api_detail"),
    path('filter/',api_filter_view.as_view(),name = "api_filter"),
    path('new/',api_new_user,name = "api_new_user"),
]