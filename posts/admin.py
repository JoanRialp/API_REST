from django.contrib import admin

from .models import Publicaciones, Following, Posts
# Register your models here.

admin.site.register(Posts)
admin.site.register(Following)
admin.site.register(Publicaciones)