"""imgrepo URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
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
from django.urls import path
from rest_framework.routers import SimpleRouter
from imgdb.views import * 
from imgdb.api.viewsets import ImageDataViewSet, ImageTransactionViewSet

router = SimpleRouter()
router.register(r'data', ImageDataViewSet, basename='img-data')
router.register(r'transaction', ImageTransactionViewSet, basename='img-transaction')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', login_user),
    path('login/', login_user, name="login_user"),
    path('signup/', create_user, name="signup_user"),
    path('delete/', delete_user, name="user_deleted"),
    path('logout/', logout_user, name="logout_user"),
    path('dashboard/', dashboard, name="user_dashboard"),
    path('perform-logout/', perform_logout, name="perform_logout")
]

urlpatterns += router.urls