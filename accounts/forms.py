from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from tracker.models import UserProfile


class RegisterForm(UserCreationForm):
    first_name = forms.CharField(max_length=50, required=True, widget=forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'First Name'}))
    last_name = forms.CharField(max_length=50, required=False, widget=forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Last Name'}))
    email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={'class': 'form-input', 'placeholder': 'Email Address'}))

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email', 'password1', 'password2']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Username'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password1'].widget.attrs.update({'class': 'form-input', 'placeholder': 'Password'})
        self.fields['password2'].widget.attrs.update({'class': 'form-input', 'placeholder': 'Confirm Password'})


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['age', 'gender', 'occupation']
        widgets = {
            'age': forms.NumberInput(attrs={'class': 'form-input', 'min': 10, 'max': 100}),
            'gender': forms.Select(choices=[('', 'Prefer not to say'), ('male', 'Male'), ('female', 'Female'), ('non_binary', 'Non-binary'), ('other', 'Other')], attrs={'class': 'form-input'}),
            'occupation': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'e.g. Student, Engineer, Teacher'}),
        }
