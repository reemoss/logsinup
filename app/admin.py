from django.contrib import admin
from django.utils.html import format_html
from .models import DroneUser
from .models import ImageWithDetails
from .models import Gallery

@admin.register(DroneUser)
class DroneUser(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'email', 'involvement_type')
    search_fields = ('first_name', 'last_name', 'email')
    list_filter = ('involvement_type',)


@admin.register(ImageWithDetails)
class ImageWithDetailsAdmin(admin.ModelAdmin):
    list_display = ('title', 'description')
    search_fields = ('title', 'description')

@admin.register(Gallery)
class GalleryAdmin(admin.ModelAdmin):
    list_display = ('id', 'image_preview', 'created_at')
    list_display_links = ('id', 'image_preview')
    readonly_fields = ('created_at', 'image_preview')
    ordering = ('-created_at',)

    def image_preview(self, obj):
        """Generate preview of image in admin list view"""
        if obj.image:
            return format_html(
                '<img src="{}" width="100" />',
                obj.image.url
            )
        return "No Image"
    
    image_preview.short_description = 'Preview'

    def save_model(self, request, obj, form, change):
        """Log who created/modified the image"""
        if not change:
            obj.created_by = request.user
        super().save_model(request, obj, form, change)
