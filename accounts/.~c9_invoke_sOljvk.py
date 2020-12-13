from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import Userhistory, Uservisitedreview

class CustomUserCreationForm(UserCreationForm):
    rrn = forms.IntegerField(
        help_text='11자리를 입력하세요',
        label='주민등록번호',
        )

    class Meta:
        model = get_user_model()
        fields = ['username', 'rrn', 'age', 'nickname']
        exclude = ['age',]


class UserhistoryForm(forms.ModelForm):
    class Meta:
        model = Userhistory
        fields = '__all__'
        exclude = ['user', 'movie_pk']


class UservisitedreviewForm(forms.ModelForm):
    class Meta:
        model = Uservisitedreview
        fields = '__all__'
        exclude = ['user', 'review', 'visited_time']