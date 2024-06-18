from django import forms
from .models import Post, Comment
from django.contrib.auth import get_user_model
from django.forms import ModelForm

User = get_user_model()


class PostForm(ModelForm):
    created_date = forms.DateTimeField(
        input_formats=['%Y-%m-%d %H:%M:%S'],
        widget=forms.DateTimeInput(
            attrs={'class': 'form-control', 'type': 'datetime-local'}
        )
    )

    class Meta:
        model = Post
        fields = ['title', 'content', 'author', 'created_date', 'image']


class CommentForm(forms.ModelForm):
    content = forms.CharField(
        label='Comment',
        widget=forms.Textarea(attrs={
            'class': 'bg-gray-100 border border-gray-300 rounded-lg py-2 px-4 block w-full'
                     ' focus:outline-none focus:ring focus:ring-blue-500',
            'rows': '4',
            'required': True,
        })
    )
    author = forms.ModelChoiceField(
        label='Author',
        queryset=User.objects.all(),
        widget=forms.Select(attrs={
            'class': 'bg-gray-100 border border-gray-300 rounded-lg py-2 px-4 block w-full'
                     ' focus:outline-none focus:ring focus:ring-blue-500',
            'required': True,
        })
    )

    class Meta:
        model = Comment
        fields = ['author', 'content']
