from django import forms
from django.contrib.auth.models import User
from blog.models import Post, Comment

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('title', 'content', 'featured_image', 'tags')
        widgets = {
            'title': forms.TextInput(attrs={'class': 'w-full p-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-purple-corallite'}),
            'content': forms.Textarea(attrs={'class': 'w-full p-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-purple-corallite', 'rows': 10}),
            'featured_image': forms.ClearableFileInput(attrs={'class': 'w-full p-3 border border-gray-300 rounded-lg'}),
            'tags': forms.SelectMultiple(attrs={'class': 'w-full p-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-purple-corallite'}),
        }

class ProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email')
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'w-full p-3 border rounded-lg focus:outline-none focus:ring-2 focus:ring-purple-corallite'}),
            'last_name': forms.TextInput(attrs={'class': 'w-full p-3 border rounded-lg focus:outline-none focus:ring-2 focus:ring-purple-corallite'}),
            'email': forms.EmailInput(attrs={'class': 'w-full p-3 border rounded-lg focus:outline-none focus:ring-2 focus:ring-purple-corallite'}),
        }

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('content',)
