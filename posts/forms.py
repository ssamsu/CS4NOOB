from django import forms
from pagedown.widgets import PagedownWidget
from .models import Post, Feedback

class Post_form(forms.ModelForm):
    content = forms.CharField(widget=PagedownWidget(show_preview=False))
    class Meta:
        model = Post
        fields = ["title", "content", "image", "category", "draft"]

class Feedback_form(forms.ModelForm):
    class Meta:
        model = Feedback
        fields = ["email", "name", "message"]
