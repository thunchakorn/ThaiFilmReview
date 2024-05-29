from django.contrib import admin

from .models import Genre, Person, Film, Role, Link


class FilmAdmin(admin.ModelAdmin):
    search_fields = ["name"]


admin.site.register(Genre)
admin.site.register(Person)
admin.site.register(Film, FilmAdmin)
admin.site.register(Role)
admin.site.register(Link)
