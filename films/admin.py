from django.contrib import admin

from .models import Genre, Person, Film, Role

admin.site.register(Genre)
admin.site.register(Person)
admin.site.register(Film)
admin.site.register(Role)
