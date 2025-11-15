from django.contrib import admin
from .models import Community, UsersAllowed

# Register your models here.

admin.site.register(Community)
admin.site.register(UsersAllowed)
