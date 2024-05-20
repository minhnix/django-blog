from .models import Post, Tag, Comment
from django import forms

from martor.fields import MartorFormField


class SimpleForm(forms.Form):
    title = forms.CharField(widget=forms.TextInput())
    description = MartorFormField()
    wiki = MartorFormField()


class PostForm(forms.ModelForm):
    tag_names = forms.CharField(max_length=1000, required=False, help_text="Enter tags separated by commas")

    class Meta:
        model = Post
        fields = ['title', 'description', 'thumbnail']  # Loại bỏ trường 'id'

    # def save(self, commit=True):
    #     post = super().save(commit=False)
    #     tag_names = self.cleaned_data.get('tag_names')
    #     if tag_names:
    #         tag_names = [tag.strip() for tag in tag_names.split(',')]
    #         post.save()
    #         post.tags.add(*tag_names)
    #     else:
    #         post.save()
    #     return post

class TagForm(forms.ModelForm):
    class Meta:
        model = Tag
        fields = "__all__"

class CommentForm(forms.ModelForm):
    parent_id = forms.IntegerField(widget=forms.HiddenInput(), required=False)
    class Meta:
        model = Comment
        fields = ('content', 'parent_id')
