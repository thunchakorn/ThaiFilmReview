from django.contrib import admin
from reviews.models import Review, Comment, Like


class CommentInline(admin.TabularInline):
    model = Comment
    extra = 1


class ReviewAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {"fields": ["profile", "film"]}),
        (
            "Rating",
            {
                "fields": [
                    "rating",
                    "screenplay_rating",
                    "acting_rating",
                    "production_rating",
                    "cinematography_rating",
                ]
            },
        ),
        ("Review", {"fields": ["is_spoiler", "short_review", "full_review"]}),
    ]
    list_display = ["__str__", "is_spoiler"]
    inlines = [CommentInline]


admin.site.register(Review, ReviewAdmin)
admin.site.register(Comment)
admin.site.register(Like)
