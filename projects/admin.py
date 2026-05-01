from django.contrib import admin
from .models import Project, Review, Tag


admin.site.register(Project)
admin.site.register(Review)

@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('name', 'is_approved', 'created')
    list_editable = ('is_approved',)
    list_filter = ('is_approved', 'created')
    search_fields = ('name',)
    ordering = ('name',)
