from django.contrib import admin
from main_app.models import Donation, Institution, Category

# Register your models here.


def indexes_of_categories(obj):
    result = []
    for category in obj.categories.all():
        result.append(category.id)
    return result


class InstitutionAdmin(admin.ModelAdmin):
    list_display = ['name', indexes_of_categories]


admin.site.register(Donation)
admin.site.register(Category)
admin.site.register(Institution, InstitutionAdmin)
