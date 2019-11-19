from django import forms
from django.db.models import Q
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.contrib.auth import get_user_model
User = get_user_model()

# Create user
class UserCreationForm(forms.ModelForm):
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
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

    def save(self, commit=True):
        user = super(UserCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data['password1'])
        
        if commit:
            user.save()
        
        return user

# Update user
class UserChangeForm(forms.ModelForm):
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = User
        fields = ('email', 'password', 'is_active', 'gender')

    def clean_password(self):
        return self.initial['password']


class UserLoginForm(forms.Form):
    query = forms.CharField(label='Email')
    password = forms.CharField(label='Password', widget=forms.PasswordInput)

    def clean(self, *args, **kwargs):
        query = self.cleaned_data.get('query')
        password = self.cleaned_data.get('password')
        user_qs_final = User.objects.filter(
            Q(username__iexact=query) |
            Q(email__iexact=query)
        ).distinct()

        if not user_qs_final.exists() and user_qs_final.count != 1:
            raise forms.ValidationError("Invalid credentials - user does not exist")
        
        user_obj = user_qs_final.first()
        
        if not user_obj.Check_password(password):
            raise forms.ValidationError("credentials are not correct")
        
        self.cleaned_data["user_obj"] = user_obj
        return super(UserLoginForm, self).clean(*args, **kwargs)