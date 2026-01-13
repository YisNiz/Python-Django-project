from django.contrib import admin

from Django_App.models import CustomUser,Task,Team

# Register your models here.
admin.site.register(Task)
admin.site.register(Team)
admin.site.register(CustomUser)

