from django.contrib import admin
from .models import Task, ContextEntry, Category

@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'priority_score', 'status', 'deadline')
    list_filter = ('status', 'priority_score', 'category')
    search_fields = ('title', 'description')


@admin.register(ContextEntry)
class ContextEntryAdmin(admin.ModelAdmin):
    list_display = ('source_type', 'timestamp', 'content', 'short_insights')
    readonly_fields = ('processed_insights',)

    def short_content(self, obj):
        return obj.content[:50] + "..." if len(obj.content) > 50 else obj.content

    def short_insights(self, obj):
        return obj.processed_insights[:50] + "..." if obj.processed_insights and len(obj.processed_insights) > 50 else obj.processed_insights

    short_content.short_description = "Context"
    short_insights.short_description = "Insights"


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'usage_frequency')
    search_fields = ('name', 'tags')