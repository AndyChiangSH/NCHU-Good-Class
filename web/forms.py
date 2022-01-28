from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .views import Profile, Department


# 修改個人系所表單
class ProfileDeptForm(forms.Form):
    dept = forms.ModelChoiceField(
        label="你的系所",
        widget=forms.Select(attrs={'class': 'form-control'}),
        queryset=Department.objects.all().order_by("dDept"),
    )
