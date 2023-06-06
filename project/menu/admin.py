from django.contrib import admin
from .models import Menu

@admin.register(Menu)
class MenuAdmin(admin.ModelAdmin):
    fields = ['menu_name', 'name', 'url', 'order']
    list_display = ('name', 'url', 'order', 'menu_name')
    list_filter = ('menu_name',)
    search_fields = ('name', 'url')

# Register your models here.
