from django import forms
from django.contrib.auth.forms import ReadOnlyPasswordHashField

from .models import User


class LoginForm(forms.Form):
    email = forms.EmailField(label='Your Email')
    password = forms.CharField(widget=forms.PasswordInput)

class VerifyForm(forms.Form):
    key = forms.IntegerField(label='Enter key')

class RegisterForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    password2 = forms.CharField(label='Confirm password', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('email', )
       
    def clean_email(self):
        email = self.cleaned_data.get('email')
        qs = User.objects.filter(email=email)
        
        if qs.exists():
            raise forms.ValidationError("This email is used")
        return email

    def clean_password(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords didn't match")
        return password2



class TempRegisterForm(forms.Form):
    email = forms.EmailField()
    key = forms.IntegerField()

class SetPasswordForm(forms.Form):
    password = forms.CharField(widget=forms.PasswordInput)
    password2 = forms.CharField(label='Confirm password', widget=forms.PasswordInput)



class UserAdminCreationForm(forms.ModelForm):
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Confirm password', widget=forms.PasswordInput)
    
    class Meta:
        model = User
        fields = ('email', )

    def clean_password(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords didn't match")
        return password2

    def save(self, commit=True):
        user = super(UserAdminCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data['password1'])
        
        if commit:
            user.save()
        return user
    
class UserAdminChangeForm(forms.ModelForm):
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = User
        fields = ('email', 'password', 'active', 'admin', 'gender')

    def clean_password(self):
        return self.initial['password']