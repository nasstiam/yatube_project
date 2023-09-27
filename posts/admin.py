from django.contrib import admin

from .models import Post, Group

class PostAdmin(admin.ModelAdmin):
    # we list the fields that should be displayed in admin panel
    list_display = ('pk', 'text', 'created', 'author', 'group')
    # option to search by text field
    search_fields = ('text',)
    # filter posts by date
    list_filter = ('created',)
    empty_value_display = '-empty-'
    list_editable = ('group',)


admin.site.register(Post, PostAdmin)
admin.site.register(Group)