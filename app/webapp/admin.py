from django.contrib import admin
from django.contrib.auth.models import User
from .models import Post, Dog, Article, Featured, Reservation

# Register your models here.
admin.site.register(Post)
admin.site.register(Dog)
admin.site.register(Article)
admin.site.register(Featured)
admin.site.register(Reservation)
