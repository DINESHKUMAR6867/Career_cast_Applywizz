from django.contrib import admin
from django.utils.html import format_html
from .models import CustomUser, CareerCast


@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('email', 'first_name', 'last_name', 'is_verified', 'date_joined')
    list_filter = ('is_verified', 'is_staff', 'is_superuser')
    search_fields = ('email', 'first_name', 'last_name')
    ordering = ('-date_joined',)

    def delete_queryset(self, request, queryset):
        """Delete CareerCast objects linked to users when users are deleted."""
        for user in queryset:
            CareerCast.objects.filter(user=user).delete()
        super().delete_queryset(request, queryset)


@admin.register(CareerCast)
class CareerCastAdmin(admin.ModelAdmin):
    list_display = ('user', 'job_title', 'created_at', 'resume_link', 'video_link')
    list_filter = ('created_at', 'updated_at')
    search_fields = ('job_title', 'user__email')
    readonly_fields = ('created_at', 'updated_at')

    def resume_link(self, obj):
        """Clickable link for resume file."""
        if obj.resume_file:
            return format_html('<a href="{}" target="_blank">📄 View Resume</a>', obj.resume_file.url)
        return "—"
    resume_link.short_description = "Resume"

    def video_link(self, obj):
        """Clickable link for video file."""
        if obj.video_file:
            return format_html('<a href="{}" target="_blank">🎥 Watch Video</a>', obj.video_file.url)
        return "—"
    video_link.short_description = "Video"
