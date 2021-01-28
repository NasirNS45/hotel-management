from django.contrib import admin

admin.site.site_header = 'Admin Page'


class Admin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'email')
    list_filter = 'email'

