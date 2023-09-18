from django.contrib import admin
from .models import Institution

@admin.register(Institution)
class InstitutionAdmin(admin.ModelAdmin):
    list_display = ('name', 'type_name', 'description', 'category_list')

    def type_name(self, obj):
        return obj.get_type_display()
    type_name.short_description = 'Type'

    def category_list(self, obj):
        return ", ".join([category.name for category in obj.category.all()])
    category_list.short_description = 'Categories'