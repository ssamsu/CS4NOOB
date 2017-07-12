from django.contrib import admin
from .models import Category, Feedback, Post


class Category_admin(admin.ModelAdmin):
    list_display = ["__str__", "created"]
    list_filter = ["created", "updated"]

    class Meta():
        model = Category

class Feedback_admin(admin.ModelAdmin):
    list_display = ["__str__", "created", "message"]
    list_filter = ["created"]

    class Meta():
        model = Feedback

class Post_admin(admin.ModelAdmin):
    list_display = ["__str__", "created", "updated"]
    list_filter = ["created", "updated"]
    search_fields = ["title", "content"]

    class Meta():
        model = Post


admin.site.register(Category, Category_admin)
admin.site.register(Post, Post_admin)
admin.site.register(Feedback, Feedback_admin)

admin.site.site_title = 'CS4NOOB'
admin.site.site_header = 'CS4NOOB'
