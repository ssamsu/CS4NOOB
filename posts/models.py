from django.conf import settings
from django.core.urlresolvers import reverse
from django.db import models
from django.utils.text import slugify

from markdown_deux import markdown

# To store data about the POST Category
class Category(models.Model):
    title = models.CharField(max_length=200, verbose_name="Category")
    created = models.DateTimeField(auto_now_add=True, verbose_name="Created at")
    updated = models.DateTimeField(auto_now=True, verbose_name="Updated at")

    class Meta:
        verbose_name_plural = "Categories"
        ordering = ['title']

    def __str__(self):
        return self.title

# To store data about the Feedback coming from CONTACT Page
class Feedback(models.Model):
    email = models.EmailField(verbose_name='Your Email')
    name = models.CharField(max_length=200, verbose_name='Your Name')
    message = models.TextField(verbose_name='Message')
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.email

# To store data about Blog Post
class Post(models.Model):
    category = models.ManyToManyField(Category, verbose_name="Category")
    user = models.ForeignKey(settings.AUTH_USER_MODEL, default=1, verbose_name="Author") # default=1 is used so that by default the post is created by first user which is the superuser
    title = models.CharField(max_length=100, verbose_name="Title")
    slug = models.SlugField(unique=True)
    content = models.TextField()
    draft = models.BooleanField(default=True, verbose_name="Draft?")
    image = models.ImageField(blank=True, null=True, upload_to="img")
    created = models.DateTimeField(auto_now_add=True, verbose_name="Created at")
    updated = models.DateTimeField(auto_now=True, verbose_name="Updated at")

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        self.slug = "%s-%s" % (slugify(self.title), self.id)
        super(Post, self).save(*args, **kwargs)
