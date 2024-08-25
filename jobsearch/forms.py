from django import forms
from .models import user_table ,Opportunity
from django.contrib.auth import authenticate

class RegisterForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = user_table
        fields = ['username', 'email', 'mobile_no', 'address', 'domain' , 'about']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])
        if commit:
            user.save()
        return user

class LoginForm(forms.Form):
    username = forms.CharField(max_length=100)
    password = forms.CharField(widget=forms.PasswordInput)

    def clean(self):
        cleaned_data = super().clean()
        username = cleaned_data.get("username") 
        
        password = cleaned_data.get("password")
        
        if username and password:
            user = authenticate(username=username, password=password)
            if user is None:
                raise forms.ValidationError("Invalid username or password.")
            self.cleaned_data['user'] = user
        
        return cleaned_data 
    
class UserProfileEditForm(forms.ModelForm):
    class Meta:
        model = user_table
        fields = ['username', 'email', 'mobile_no', 'address', 'domain', 'about' ,'profile_image' , 'resume']


class OpportunityForm(forms.ModelForm):
    class Meta:
        model = Opportunity
        fields = ['title', 'type', 'domain', 'salary', 'experience', 'prerequisites', 'description', 'company_logo']