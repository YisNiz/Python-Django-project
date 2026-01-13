import datetime

from django import forms
from django.contrib.auth import authenticate
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser, Role, Task

class RegisterForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ["username", "password1", "password2"]

    def save(self, commit=True):
        user = super().save(commit=False)
        if commit:
            user.is_superuser = False
            user.is_staff = False
            user.save()
        return user


class Personal_areaForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ["role", "team"]

    def clean_team(self):
        team = self.cleaned_data.get("team")
        if team is None:
            raise ValidationError("חובה לבחור צוות למשתמש")
        return team

    def clean(self):  # בדיקה אם כבר יש מנהל לצוות
        cleaned_data = super().clean()
        role = cleaned_data.get("role")
        team = cleaned_data.get("team")
        if role == Role.ADMIN and team is not None:
            exists_other_admin = CustomUser.objects.filter(
                team=team,
                role=Role.ADMIN
            ).exists()
            if exists_other_admin:
                raise ValidationError("כבר יש מנהל לצוות הזה")
        return cleaned_data

    def save(self, commit=True):#שמירת המשתמש והגדרת המנהל לצוות
        user = super().save(commit=False)
        if commit:
            user.save()
        role = self.cleaned_data.get("role")
        team = self.cleaned_data.get("team")
        if role == Role.ADMIN and team:
            team.admin = user
            team.save()
        return user




class LoginForm(forms.Form):
    username = forms.CharField(max_length=100)
    password = forms.CharField(widget=forms.PasswordInput)

    def clean(self):
        cleaned_data = super().clean()
        username = cleaned_data.get("username")
        password = cleaned_data.get("password")
        if not username or not password:
            return cleaned_data
        user = authenticate(username=username, password=password)
        if user is None:
            raise ValidationError("שם משתמש או סיסמה לא נכונים")
        self.user = user
        return cleaned_data


class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ["name", "description", "finishDate"]
        widgets = {
            "finishDate": forms.DateInput(attrs={"type": "date"}),
        }


class UpdateTaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ["name", "description", "finishDate"]
        widgets = {
            "finishDate": forms.DateInput(attrs={"type": "date"}),
        }