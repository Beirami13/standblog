from django.contrib.auth import authenticate
from django.forms import ValidationError
from django import forms
from django.contrib.auth.models import User
from .models import Profile

class LoginForm(forms.Form):
    username = forms.CharField(max_length=200, required=False, widget=forms.TextInput(attrs={'class': 'input100'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'input100'}))

    def clean(self):
        cleaned_data = super().clean()
        username = cleaned_data.get('username')
        password = cleaned_data.get('password')
        user = authenticate(username=username, password=password)
        if user is None:
            raise ValidationError(
                'Your username or password is incorrect.',
                code='invalid_info'
            )

        return cleaned_data

class RegistrationForm(forms.Form):
    username = forms.CharField(max_length=200, required=False, widget=forms.TextInput(attrs={'class': 'input100', 'placeholder': 'Username'}))
    email = forms.EmailField(required=False, widget=forms.TextInput(attrs={'class': 'input100', 'placeholder': 'Email'}))
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'input100', 'placeholder': 'Enter Password'}))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'input100', 'placeholder': 'Repeat Password'}))

    def clean(self):
        cleaned_data = super().clean()

        username = cleaned_data.get('username')
        password1 = cleaned_data.get('password1')
        password2 = cleaned_data.get('password2')

        if not username:
            raise ValidationError("Username is required.", code='invalid_info')
        if password1 and password2 and password1 != password2:
            raise ValidationError("Passwords don't match.", code='invalid_info')
        elif password1 and len(password1) < 6:
            raise ValidationError("Password must be at least 6 characters long.", code='invalid_info')
        if username and User.objects.filter(username=username).exists():
            raise ValidationError("This username already exists.", code='invalid_info')

        return cleaned_data


from django import forms


class CreateProfileForm(forms.Form):
    first_name = forms.CharField(max_length=150,widget=forms.TextInput(attrs={'class': 'input100','placeholder': 'First Name',}))
    last_name = forms.CharField(max_length=150,widget=forms.TextInput(attrs={'class': 'input100','placeholder': 'Last Name',}))
    fathers_name = forms.CharField(max_length=100,widget=forms.TextInput(attrs={'class': 'input100','placeholder': "Father's Name",}))
    national_code = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class': 'input100','placeholder': 'National Code',}))
    image = forms.ImageField(required=False,widget=forms.ClearableFileInput(attrs={'class': 'image-input','accept': 'image/*',}))


class UserEditForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name','last_name',]
        widgets = {'first_name': forms.TextInput(attrs={'class': 'input100','placeholder': 'First Name',}),
                   'last_name': forms.TextInput( attrs={'class': 'input100','placeholder': 'Last Name',}),}


class ProfileEditForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['national_code','image',]
        widgets = {'national_code': forms.TextInput(attrs={'class': 'input100','placeholder': 'National Code', }),
                    'image': forms.ClearableFileInput(attrs={'class': 'image-input','accept': 'image/*', }), }