# django
from django import forms
from django.contrib.auth.forms import AuthenticationForm
# third
# own
from apps.user.models import User

class LoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super(LoginForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs['class']='form-control'
        self.fields['username'].widget.attrs['placeholder']='Username'
        self.fields['password'].widget.attrs['class']='form-control'
        self.fields['password'].widget.attrs['placeholder']='Password'

class UserForm(forms.ModelForm):
    password1 = forms.CharField(label='Add Password', widget=forms.PasswordInput())
    password1.widget.attrs['class']='form-control'
    password1.widget.attrs['placeholder']='Add your password.'
    password2 = forms.CharField(label='Confirm Password', widget=forms.PasswordInput())
    password2.widget.attrs['class']='form-control'
    password2.widget.attrs['placeholder']='Add your password again.'
    class Meta:
        model = User
        fields = [
            'username',
            'name',
            'lastname',
            'email',
            'image'
        ]
        labels = {
            'username':'User Username',
            'name':'User Name',
            'lastname':'User Last Name',
            'email':'User Email',
            'image': 'User Image'
        }
        widgets = {
            'username' : forms.TextInput(
                attrs = {
                    'class':'form-control',
                    'placeholder':'Enter a User Name'
                }
            ),
            'name' : forms.TextInput(
                attrs = {
                    'class':'form-control',
                    'placeholder':'Enter a Name'
                }
            ),
            'lastname' : forms.TextInput(
                attrs = {
                    'class':'form-control',
                    'placeholder':'Enter a Last Name'
                }
            ),
            'email' : forms.EmailInput(
                attrs = {
                    'class':'form-control',
                    'placeholder':'Enter a Email'
                }
            )
        }

    def clean_password2(self): # para validar un campo determinado -> clean_field.
        password1 = self.cleaned_data['password1']
        password2 = self.cleaned_data['password2']
        if (password1 and password2 and password1 != password2):
            raise forms.ValidationError('Passwords not equal.')
        return password2

    def save(self, commit=True): # commit -> que proceda con el registro.
        user = super().save(commit=False) # para tomar la instancia hasta el momento.
        user.set_password(self.cleaned_data['password2'])
        if (commit):
            user.save()
        return user