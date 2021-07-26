"""Up until this point we have used django's UserCreationForm for our registration page. Now to add additional fields we are creating a forms.py file to edit the built in form."""
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, PasswordChangeForm
from django.contrib.auth.models import User
from django import forms
from theblog.models import  Profile

class ProfilePageForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('bio', 'profile_pic','website_url','facebook_url', 'twitter_url',
        'instagram_url','pinterest_url')
        widgets = {'bio': forms.Textarea(attrs={'class': 'form-control'}),
                # 'profile_pic': forms.TextInput(attrs={'class': 'form-control'}),
                'website_url': forms.TextInput(attrs={'class': 'form-control'}),
                'facebook_url': forms.TextInput(attrs={'class': 'form-control'}),
                'twitter_url': forms.TextInput(attrs={'class': 'form-control'}),
                'instagram_url': forms.TextInput(attrs={'class': 'form-control'}),
                'pinterest_url': forms.TextInput(attrs={'class': 'form-control'}),
            }

class SignUpForm(UserCreationForm):
    # The django UserCreationForm does not have email, first_name, last_name fields. To add that we are creating a new SignUpForm and inherit the UserCreationForm and add the extra fields we want.
    # Here we use widgets to style our form.
    # In the other app we have used widget in a different way, here we can't use that since we use a built in UserCreationForm.
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control'}))
    first_name = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class': 'form-control'}))
    last_name = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class': 'form-control'}))
    class Meta():
        model = User
        fields = ('username', 'first_name', 'last_name', 'email','password1','password2')
        # Here password1 and password2 are the names django uses in the UserCreationForm
    
    # To style the 'username' and 'password' fields
    def __init__(self, *args, **kwargs):
        super(SignUpForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs['class'] = 'form-control'
        self.fields['password1'].widget.attrs['class'] = 'form-control'
        self.fields['password2'].widget.attrs['class'] = 'form-control'

# To style the edit_profile page 
class EditProfileForm(UserChangeForm):
    # Here UserChangeForm is a built in form.
    # Here we got name of the fields from view page source from the webpage.
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control'}))
    first_name = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class': 'form-control'}))
    last_name = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class': 'form-control'}))
    username = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class': 'form-control'}))
    last_login= forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class': 'form-control'}))
    is_superuser= forms.CharField(max_length=100, widget=forms.CheckboxInput(attrs={'class': 'form-check'}))
    is_staff= forms.CharField(max_length=100, widget=forms.CheckboxInput(attrs={'class': 'form-check'}))
    is_active= forms.CharField(max_length=100, widget=forms.CheckboxInput(attrs={'class': 'form-check'}))
    date_joined= forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class': 'form-control'}))
    
    
    class Meta():
        model = User
        fields = ('username', 'first_name', 'last_name', 'email','password','last_login','is_superuser','is_staff','is_active','date_joined')


# To style the password change form
class PasswordChangingForm(PasswordChangeForm):
    old_password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'type':'password'}))
    new_password1= forms.CharField(max_length=100, widget=forms.PasswordInput(attrs={'class': 'form-control', 'type':'password'}))
    new_password2= forms.CharField(max_length=100, widget=forms.PasswordInput(attrs={'class': 'form-control', 'type':'password'}))

    class Meta():
        model = User
        fields = ('old_password','new_password1','new_password2')

