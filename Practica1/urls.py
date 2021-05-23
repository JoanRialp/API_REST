"""Practica1 URL Configuration

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
from django.db import router
from django.urls.conf import include
from Practica1.constants import ROUTES
from django.shortcuts import redirect
from django.contrib import admin
from django.urls import path

from rest_framework import routers
from posts import views

router = routers.DefaultRouter()
router.register(r'publicaciones', views.PublicacionesViewSet)
router.register(r'users', views.UserViewSet)
router.register(r'posts', views.PostViewSet)
router.register(r'followings', views.FollowingViewSet)

urlpatterns = [
    path(ROUTES.ADMIN, admin.site.urls),
    path(ROUTES.INDEX, views.redirect_to_register),
    path(ROUTES.REGISTER, views.register_view),
    path(ROUTES.LOGIN, views.login_view),
    path(ROUTES.POSTS, views.post_list_view),

    path(ROUTES.PRINCIPAL, views.principal),
    path(ROUTES.PRINCIPAL_REST, views.PrincipalView_Publicaciones.as_view()),
    path(ROUTES.MANU_LATERAL_REST, views.MenuLateral_NoFollowings.as_view()),

    path(ROUTES.PERFIL, views.perfil),
    path(ROUTES.PERFIL_REST, views.PerfilView_Informacion.as_view()),

    path(ROUTES.FOLLOWING_REST, views.FollowingUsersView.as_view()),

    path('',include(router.urls))
]
