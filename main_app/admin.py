from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from main_app.models import Donation, Institution, Category


def indexes_of_categories(obj):
    result = []
    for category in obj.categories.all():
        result.append(category.id)
    return result


class InstitutionAdmin(admin.ModelAdmin):
    list_display = ['name', indexes_of_categories]


class MyUserAdmin(UserAdmin):
    def has_delete_permission(self, request, obj=None):
        if obj and ((User.objects.all().filter(is_superuser=True).count() <= 1 and obj.is_superuser) or
                    obj.id == request.user.id):
            return False
        else:
            return True


admin.site.unregister(User)
admin.site.register(User, MyUserAdmin)
admin.site.register(Donation)
admin.site.register(Category)
admin.site.register(Institution, InstitutionAdmin)
