from django.db.models import query
from rest_framework.views import APIView
from .serializers import PostsSerializer, PublicacionesSerializer, UserSerializer, FollowingSerializer
from typing import cast
from django.db import reset_queries

from django.db.models.fields import NullBooleanField
from django.db.models.query import QuerySet
from Practica1.constants import ROUTES
from django.shortcuts import redirect, render
from django.http import HttpRequest, request
from .models import Posts, Publicaciones, Following
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login

from rest_framework import viewsets, permissions
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from django.db.models import Q

"API endpoint that allow users to be viewed or edited"
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

class PublicacionesViewSet(viewsets.ModelViewSet):
    queryset = Publicaciones.objects.all()
    serializer_class = PublicacionesSerializer
    permission_classes = [permissions.AllowAny]

class PostViewSet(viewsets.ModelViewSet):
    queryset = Posts.objects.all()
    serializer_class = PostsSerializer
    permission_classes = [permissions.AllowAny]

class FollowingViewSet(viewsets.ModelViewSet):
    queryset = Following.objects.all()
    serializer_class = FollowingSerializer
    permission_classes = [permissions.AllowAny]

# Create your views here.

def post_list_view(request : HttpRequest):
    post_objs = Posts.objects.all()
    context = {
        'postlist' : post_objs,
    }
    print(request.GET)
    return render(request, 'blog/posts.html', context)

def redirect_to_register(request : HttpRequest):
    return redirect(ROUTES.REGISTER)

def register_view(request : HttpRequest):
    print(request.POST)

    context ={
        'LOGINVIEW' : "/"+ROUTES.LOGIN
    }
    if request.POST:
        username = request.POST["username"]
        password = request.POST["password"]
        email = request.POST["email"]
        fname = request.POST["firstname"]
        lname = request.POST["lastname"]
        print("asdasdasdas")
        try :
            user = User.objects.create_user(username, email, password)
            user.first_name= fname
            user.last_name = lname
            user.save()
            user = authenticate(username=username, password=password)
            if user is not None:
                request.user = user
                login(request,user)
                Following.objects.create(id_user = request.user.id, id_UserFlollowing = request.user.id)
                return redirect("/" +ROUTES.PRINCIPAL)
            else:
                print('Algo salió mal...')
        except :
            if User.objects.filter(username=username).exists():
                print('¡Ya existe un usuario con ese nombre!')
            if User.objects.filter(email=email).exists():
                print(request,'¡Ya existe un usuario con ese email!')
    return render(request, 'register.html',context)

def login_view(request : HttpRequest):
    context ={
        'REGISTERVIEW' : "/" + ROUTES.REGISTER,
        'PRINCIPALVIEW' : "/" + ROUTES.PRINCIPAL
    }
    if request.POST:
        username = request.POST["username"]
        password = request.POST["password"]
        print(username)
        print(password)
        user = authenticate(username=username, password=password)
        print(user)
        if user is not None:
            request.user = user
            login(request,user)
            print("Session: ", request.session)
            return redirect("/" +ROUTES.PRINCIPAL)
        else:
            print('Algo salió mal...')
    return render(request, 'login.html', context)


#API REST

#Usuarios Following
class FollowingUsersView(APIView):

    def get(self, request):
        followings = Following.objects.filter(id_user = request.user.id and ~Q(id_UserFlollowing =  request.user.id)).values_list('id_UserFlollowing', flat=True)[:5]
        print(followings)

        users = User.objects.filter(id__in = followings)
        print(users)

        serialized = UserSerializer(users, many=True)
        return Response(serialized.data)

    def delete(self, request, pk=None, format=None):
        usuarioFollowing = request.data.get("id_UserFlollowing")
        print(usuarioFollowing)

        Following.objects.filter(id_user = request.user.id, id_UserFlollowing = usuarioFollowing).delete()

        return Response(status=status.HTTP_204_NO_CONTENT)

#Menu Lateral: GET, POST
class MenuLateral_NoFollowings(APIView):

    def get(self, request):
        followings = Following.objects.filter(id_user = request.user.id).values_list('id_UserFlollowing', flat=True)[:5]
        print(followings)

        users = User.objects.filter(~Q(id__in = followings))
        print(users)

        serialized = UserSerializer(users, many=True)
        return Response(serialized.data)

    def post(self, request):
        print(request)
        serializer = FollowingSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#Publicaciones: GET, POST, PUT y DELETE
class PrincipalView_Publicaciones(APIView):
    
    def get(self, request):
        followings = Following.objects.filter(id_user = request.user.id).values_list('id_UserFlollowing', flat=True)
        print("Foll",followings)

        #Publicaciones de los usuarios que sigue el usuario y sus publicacionese
        publicaciones = Publicaciones.objects.filter(id_user__in = followings).order_by('-id')

        print("Posts: ", publicaciones)

        serialized = PublicacionesSerializer(publicaciones, many=True)
        return Response(serialized.data)

    def post(self, request):
        print(request)
        serializer = PublicacionesSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk=None, format=None):
        id_publicacion = request.data.get("id")
        print(id_publicacion)
        publicacion = Publicaciones.objects.filter(pk = id_publicacion).first()
        print(publicacion)

        serializer = PublicacionesSerializer(publicacion, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, pk=None, format=None):
        id_publicacion = request.data.get("id")
        Publicaciones.objects.filter(id = id_publicacion).delete()

        return Response(status=status.HTTP_204_NO_CONTENT)

#Perfil Usuario
class PerfilView_Informacion(APIView):

    def get(self, request):
        me = request.user

        usuario = User.objects.filter(id = me.id)

        serialized = UserSerializer(usuario, many=True)
        return Response(serialized.data)

    def put(self, request, pk=None, format=None):
        me = request.user

        usuario = User.objects.filter(id = me.id)
        print(usuario)

        #editar_usuario['username'] = [usuario[0].username]
        #editar_usuario['password'] = [usuario[0].password]

        User.objects.filter(id=me.id).update(first_name = request.data["first_name"], last_name = request.data["last_name"], email = request.data["email"])
        return Response(request.data)
        #serializer = UserSerializer(usuario, editar_usuario, many=True)
        #if serializer.is_valid():
            #serializer.save()
            #return Response(serializer.data)
        #return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


#Views
def perfil(request : HttpRequest):
        usuario = request.user
        print("perfil")
        context ={
            'User': usuario,
            'PRINCIPALVIEW' : "/"+ROUTES.PRINCIPAL,
            'LOGINVIEW' : "/"+ROUTES.LOGIN,
        }

        return render(request, 'perfil.html', context)

def principal(request):
        usuario = request.user

        context ={
            'User': usuario,
            'PERFILVIEW' : "/"+ROUTES.PERFIL,
            'LOGINVIEW' : "/"+ROUTES.LOGIN,
        }

        return render(request, 'principal.html', context)