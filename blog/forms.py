from django import forms
from .models import Post

class CreateBlogPostForm(forms.ModelForm):
    class Meta:
        model=Post
        fields = ['title', 'head0', 'chead0', 'head1', 'chead1', 'head2', 'chead2', 'thumbnail', 'video', 'content']