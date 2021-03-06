"""mentor URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include
# from user.views import home_view,api_filter_view,api_detail_view
app_name = "mentor"
urlpatterns = [
    path('admin/', admin.site.urls),
    # path('user/',include('user.urls')),
    path('api/',include('api.urls',namespace="api")),
    # path('',home_view,name="home"),
    # path('api/',api_filter_view.as_view(),name="api"), 
    # path('api/<str:regno>',api_detail_view,name="detail"), 
]
