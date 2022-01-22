from django.contrib import admin
from .models import Profile, User, Contact,LoggedInUser
# Register your models here.


admin.site.register(User)
admin.site.register(Profile)
admin.site.register(Contact)
admin.site.register(LoggedInUser)
