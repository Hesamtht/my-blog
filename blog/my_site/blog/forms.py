from django import forms
from .models import *

class AccountForm(forms.Form):
    GENDER = (
        ('آقا' , 'آقا'),
        ('خانم' , 'خانم')
    )
    name = forms.CharField(max_length = 25 , required = False , label = 'نام')
    last_name = forms.CharField(max_length = 50 , required = False , label = 'نام خانوادگی')
    gender = forms.ChoiceField(choices = GENDER , widget = forms.RadioSelect , label = 'جنسیت')
    address = forms.CharField(max_length = 250 , widget = forms.Textarea , label = 'آدرس')
    phone = forms.CharField(max_length = 11 , required = True , label = 'شماره')
    age = forms.IntegerField(label = 'سن')


    def clean_phone(self):
        phone = self.cleaned_data['phone']
        if phone:
            if not phone.isnumeric():
                raise forms.ValidationError('شماره تلفن باید عددی باشد')
            else:
                return phone #return phone number if there's no error

    def clean_age(self):
        age = self.cleaned_data['age']
        if age:
            if age < 0:
                raise forms.ValidationError('سن نباید عدد منفی باشد')
            else:
                return age


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('name', 'email', 'body')


class UserRegistrationForm(forms.Form):
    username = forms.CharField(label = 'نام کاربری')
    password = forms.CharField(label = 'رمز عبور')
    email = forms.EmailField(label = 'ایمیل')


class UserLoginForm(forms.Form):
    username = forms.CharField(label = 'نام کاربری')
    password = forms.CharField(label = 'رمز عبور')

    def clean_user(self):
        if username is None:
            raise forms.ValidationError('کادر نام کاربری خالی است')
    def clean_pass(self):
        if password is None:
            raise forms.ValidationError('کادر رمز عبور خالی است')


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'slug', 'body', 'status', 'publish']