from django.contrib import admin

from . import models


# Register your models here.
@admin.register(models.Role)
class RoleAdmin(admin.ModelAdmin):
    list_display = ['name', 'description']

@admin.register(models.User)
class Admin(admin.ModelAdmin):
    list_display = ['id', 'username', 'role']