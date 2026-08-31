from django import forms
from .models import Post

class ContactUsForm(forms.Form):
    name = forms.CharField(max_length=100)
    email = forms.EmailField()
    subject = forms.CharField(max_length=200, required=False)
    message = forms.CharField(max_length=500)


class PostForm(forms.ModelForm):

    class Meta:
        model = Post

        fields = [
            'title',
            'category',
            'content',
            'image',
            'pub_date',
        ]

        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'input100',
                'placeholder': 'Post title',
            }),

            'category': forms.SelectMultiple(attrs={
                'class': 'input100',
            }),

            'content': forms.Textarea(attrs={
                'class': 'input100',
                'placeholder': 'Write your post...',
                'rows': 6,
            }),

            'image': forms.ClearableFileInput(attrs={
                'class': 'input100',
            }),

            'pub_date': forms.DateTimeInput(
                attrs={
                    'class': 'input100',
                    'type': 'datetime-local',
                }
            ),
        }

