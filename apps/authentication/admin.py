from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from apps.authentication.models import UserProfile, BanHistory


class UserProfileInline(admin.StackedInline):
    model = UserProfile
    can_delete = False
    verbose_name_plural = 'Profile'
    fk_name = 'user'


class UserAdmin(BaseUserAdmin):
    inlines = (UserProfileInline,)
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_active', 'is_staff', 'date_joined')
    list_filter = ('is_active', 'is_staff', 'is_superuser', 'date_joined')
    search_fields = ('username', 'email', 'first_name', 'last_name')
    ordering = ('-date_joined',)


class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'nationality', 'phone_number', 'created_at', 'updated_at')
    list_filter = ('nationality', 'created_at')
    search_fields = ('user__username', 'user__email', 'phone_number', 'nationality')
    readonly_fields = ('created_at', 'updated_at')
    
    fieldsets = (
        ('User Information', {
            'fields': ('user',)
        }),
        ('Profile Details', {
            'fields': ('phone_number', 'nationality', 'address', 'bio')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


class BanHistoryAdmin(admin.ModelAdmin):
    list_display = ('user', 'banned_by', 'reason', 'banned_at', 'is_active')
    list_filter = ('is_active', 'banned_at')
    search_fields = ('user__username', 'banned_by__username', 'reason')
    readonly_fields = ('banned_at',)
    ordering = ('-banned_at',)
    
    fieldsets = (
        ('Ban Information', {
            'fields': ('user', 'banned_by', 'is_active')
        }),
        ('Details', {
            'fields': ('reason', 'banned_at')
        }),
    )


# Unregister the default User admin and register our custom one
admin.site.unregister(User)
admin.site.register(User, UserAdmin)
admin.site.register(UserProfile, UserProfileAdmin)
admin.site.register(BanHistory, BanHistoryAdmin)

# Customize admin site header
admin.site.site_header = "PitTalk Admin Panel"
admin.site.site_title = "PitTalk Admin"
admin.site.index_title = "Welcome to PitTalk Administration"