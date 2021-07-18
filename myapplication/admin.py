from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, Applicant, Applicationpapers, Messages, Skills, Jobs


class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ['username', 'first_name', 'last_name']
    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('anrede', 'unternehmen', 'plz', 'ort',)}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        (None, {'fields': ('anrede', 'unternehmen', 'plz', 'ort',)}),
    )


admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Applicant)
admin.site.register(Applicationpapers)
admin.site.register(Messages)
admin.site.register(Skills)
admin.site.register(Jobs)
