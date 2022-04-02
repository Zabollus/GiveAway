from django.contrib import admin
from main_app.models import Donation, Institution, Category

# Register your models here.

admin.site.register(Donation)
admin.site.register(Category)
admin.site.register(Institution)
