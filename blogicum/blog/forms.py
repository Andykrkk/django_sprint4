from django import forms

from blog.models import Comment, Post, User

TEXT_AREA_COLS = 10
TEXT_AREA_ROWS = 4


class PostForm(forms.ModelForm):

    class Meta:
        model = Post
        exclude = ('author',)
        widgets = {
            'pub_date': forms.DateTimeInput(
                format='%Y-%m-%d',
                attrs={'type': 'date'}
            )
        }


class CommentForm(forms.ModelForm):

    text = forms.CharField(
        widget=forms.Textarea(attrs={'cols': TEXT_AREA_COLS,
                                     'rows': TEXT_AREA_ROWS})
    )

    class Meta:
        model = Comment
        fields = ('text',)


class ProfileForm(forms.ModelForm):

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email']
