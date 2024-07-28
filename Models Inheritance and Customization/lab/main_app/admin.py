from django.contrib import admin

from main_app.models import Veterinarian


# Register your models here.
@admin.register(Veterinarian)
class VeterinarianAdmin(admin.ModelAdmin):
    pass
