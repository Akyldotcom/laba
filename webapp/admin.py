from django.contrib import admin

from webapp.models import Product, Category

admin.site.register(Category)


class ProductAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'description', 'created_at']
    list_display_links = ['id', 'name']
    list_filter = ['cost']
    search_fields = ['name', 'description']
    fields = ['name', 'description', 'category', 'cost', 'image']
    readonly_fields = ['created_at', 'updated_at']


admin.site.register(Product, ProductAdmin)
