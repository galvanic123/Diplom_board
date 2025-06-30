from django.contrib import admin
from .models import Advertisement, Comment, Category

admin.site.register(Advertisement)
admin.site.register(Comment)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "slug", "created_at")  # Теперь created_at существует
    list_filter = ("created_at",)  # Теперь можно фильтровать по этому полю
    prepopulated_fields = {"slug": ("name",)}
    search_fields = ("name", "slug")
    date_hierarchy = "created_at"  # Теперь можно и
