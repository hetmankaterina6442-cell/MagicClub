from django.contrib import admin
from .models import Profile

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ("user", "display_name", "country", "gender", "age_group", "newsletter_opt_in")
    search_fields = ("user__username", "display_name", "country")
    list_filter = ("gender", "age_group", "newsletter_opt_in")
