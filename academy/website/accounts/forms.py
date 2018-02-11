from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm

from academy.apps.accounts.models import User


class CustomAuthenticationForm(AuthenticationForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget = forms.TextInput(attrs={'placeholder': 'Email or Username'})
        self.fields['password'].widget = forms.PasswordInput(attrs={'placeholder': 'Password'})


class SignupForm(UserCreationForm):
    email = forms.EmailField(max_length=200)

    class Meta:
        model = User
        fields = ('email', 'username', 'password1', 'password2')

    def save(self, *args, **kwargs):
        user = super().save(commit=False)
        user.is_active = False
        user.role = User.ROLE.student
        user.save()
        user.notification_register()

        return user
