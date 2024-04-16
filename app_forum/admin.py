from django.contrib import admin
from .models import CustomUser, Topic, Comment, Category

# Register your models here.
admin.site.register(CustomUser)
admin.site.register(Topic)
admin.site.register(Comment)
admin.site.register(Category)
