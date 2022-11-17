from django import forms
from .models import News
import re
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from captcha.fields import CaptchaField


class ContactForm(forms.Form):
    subject = forms.CharField(label='Theme', widget=forms.TextInput(attrs={"class": "form-control"}))
    content = forms.CharField(label='Body', widget=forms.Textarea(attrs={"class": "form-control", "rows": 5}))
    captcha = CaptchaField()


class UserLoginForm(AuthenticationForm):
    username = forms.CharField(label='Username', widget=forms.TextInput(attrs={"class": "form-control"}))
    password = forms.CharField(label='Password', widget=forms.PasswordInput(attrs={"class": "form-control"}))


class UserRegisterForm(UserCreationForm):
    username = forms.CharField(label='Username', widget=forms.TextInput(attrs={"class": "form-control"}))
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput(attrs={"class": "form-control"}))
    password2 = forms.CharField(label='Confirm password', widget=forms.PasswordInput(attrs={"class": "form-control"}))
    email = forms.EmailField(label='Email', widget=forms.EmailInput(attrs={"class": "form-control"}))

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


class NewsForm(forms.ModelForm):
    class Meta:
        model = News
        # fields = '__all__'
        fields = ['title', 'content', 'is_published', 'category']
        widgets = {
            'title': forms.TextInput(attrs={"class": "form-control"}),
            'content': forms.Textarea(attrs={
                                  "class": "form-control",
                                  "rows": 5
                              }),
            'is_published': forms.NullBooleanSelect(attrs={"class": "form-control"}),
            'category': forms.Select(attrs={"class": "form-control"}),
        }

    # кастомный валидотор
    def clean_title(self):
        title = self.cleaned_data['title']
        if re.match(r'\d', title):
            raise ValidationError('The title should not start with a number')
        return title


    # # Форма, которая не связана с моделью:
    # title = forms.CharField(max_length=150,
    #                         widget=forms.TextInput(attrs={"class": "form-control"}))
    #
    # content = forms.CharField(required=False, label='Text',
    #                           widget=forms.Textarea(attrs={
    #                               "class": "form-control",
    #                               "rows": 5
    #                           }))
    #
    # is_published = forms.BooleanField(initial=True,
    #                                   widget=forms.NullBooleanSelect(attrs={"class": "form-control"}))
    #
    # category = forms.ModelChoiceField(queryset=Category.objects.all(), label='Topic',
    #                                   empty_label='Select a category',
    #                                   widget=forms.Select(attrs={"class": "form-control"}))
