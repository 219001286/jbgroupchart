from django.contrib import admin
from .models import Department,Topic,Message,User
# Register your models here.

admin.site.register(Department)
admin.site.register(Topic)
admin.site.register(Message)
admin.site.register(User)
    