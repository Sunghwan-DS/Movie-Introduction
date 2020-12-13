from django import forms
from .models import Review, Comment, Reply, Moviehistory, Reviewhistory


class ReviewForm(forms.ModelForm):
    title = forms.CharField(
                widget=forms.Textarea(
                        attrs={
                            'rows': 1,
                            'cols': 50,
                        }
                    ),
                label='제목',
            )


    content = forms.CharField(
                widget=forms.Textarea(
                        attrs={
                            'rows': 15,
                            'cols': 50,
                        }
                    ),
                label='내용',

            )

    rank = forms.IntegerField(
        help_text='<평점은 1점부터 10점까지 가능합니다.>',
        widget=forms.Textarea(
                        attrs={
                            'rows': 1,
                            'cols': 50,
                        }
                    ),
        label='평점',
        min_value = 1,
        max_value = 10
        )

    class Meta:
        model = Review
        exclude = ['user', 'movie', 'hit', 'like_users', 'dislike_users', 'user_hit_time']

# class CommentForm(forms.ModelForm):
#     class Meta:
#         model = Comment
#         exclude = ['user']

class CommentForm(forms.ModelForm):
    content = forms.CharField(
                widget=forms.Textarea(
                        attrs={
                            'rows': 1,
                            'cols': 50,
                        }
                    ),
                label='댓글',
            )

    class Meta:
        model = Comment
        exclude = ['user', 'review', 'like_users', 'dislike_users']


class ReplyForm(forms.ModelForm):
    content = forms.CharField(
                widget=forms.Textarea(
                        attrs={
                            'rows': 1,
                            'cols': 60,
                        }
                    ),
                label='답글',
            )

    class Meta:
        model = Reply
        exclude = ['user', 'comment', 'like_users', 'dislike_users']


class MoviehistoryForm(forms.ModelForm):
    class Meta:
        model = Moviehistory
        fields = '__all__'
        exclude = ['movie']

class ReviewhistoryForm(forms.ModelForm):
    class Meta:
        model = Reviewhistory
        fields = '__all__'
        exclude = ['review']