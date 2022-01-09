from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .views import Profile, Department


class RegisterForm(UserCreationForm):
    username = forms.CharField(
        label="電子郵件",
        widget=forms.EmailInput(attrs={'class': 'form-control'})
    )
    password1 = forms.CharField(
        label="密碼",
        widget=forms.PasswordInput(attrs={'class': 'form-control'})
    )
    password2 = forms.CharField(
        label="確認密碼",
        widget=forms.PasswordInput(attrs={'class': 'form-control'})
    )


class LoginForm(forms.Form):
    username = forms.CharField(
        label="電子郵件",
        widget=forms.EmailInput(attrs={'class': 'form-control'})
    )
    password = forms.CharField(
        label="密碼",
        widget=forms.PasswordInput(attrs={'class': 'form-control'})
    )


class ProfileDeptForm(forms.Form):
    dept = forms.ModelChoiceField(
        label="你的系所",
        widget=forms.Select(attrs={'class': 'form-control'}),
        queryset=Department.objects.all().order_by("dDept"),
    )