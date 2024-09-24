from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, SubscriptionPlan

class CustomUserAdmin(UserAdmin):
    model = CustomUser
    fieldsets = UserAdmin.fieldsets + (
        ('Additional Info', {'fields': ('is_activated', 'subscription_plan', 'subscription_end_date')}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Additional Info', {'fields': ('is_activated', 'subscription_plan', 'subscription_end_date')}),
    )

    list_display = UserAdmin.list_display + ('is_activated', 'subscription_plan', 'subscription_end_date')

admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(SubscriptionPlan)