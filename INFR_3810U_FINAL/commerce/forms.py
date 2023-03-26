from django import forms
from .models import User, Listing, Review
from django.contrib.auth.forms import UserCreationForm

class MyUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

    def __init__(self, *args, **kwargs):
        super(MyUserCreationForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs = {'class': 'form-control', 'placeholder':'Username'}
        self.fields['email'] = forms.EmailField(max_length=64, required=True, help_text='Required. Enter a valid email address.', widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder':'Email'}))
        self.fields['password1'].widget.attrs = {'class': 'form-control', 'placeholder':'Password'}
        self.fields['password2'].widget.attrs = {'class': 'form-control', 'placeholder':'Password Confirmation'}

class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('username', 'email', 'address', 'postal_code', 'country')
    def __init__(self, *args, **kwargs):
        super(UserUpdateForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs = {'class': 'form-control', 'placeholder':'Username'}
        self.fields['email'].widget.attrs = {'class': 'form-control', 'placeholder':'Email'}
        self.fields['address'].widget.attrs = {'class': 'form-control', 'placeholder':'Address'}
        self.fields['postal_code'].widget.attrs = {'class': 'form-control', 'placeholder':'XXXXXX'}
        self.fields['country'].widget.attrs = {'class': 'form-control', 'placeholder':'Country'}
        self.fields['username'].help_text = None

class ListingForm(forms.ModelForm):
    class Meta:
        model = Listing
        exclude = ('user',)
        widgets = {
            'name': forms.TextInput(attrs={'class':'form-control', 'placeholder':'Name'}),
            'price': forms.TextInput(attrs={'class':'form-control', 'placeholder':'$100'}),
            'description': forms.TextInput(attrs={'class':'form-control', 'placeholder':'Description'}),
            'image': forms.TextInput(attrs={'class':'form-control', 'placeholder':'URL to image'})
        }

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        exclude = ('user','listing')
        widgets = {
            'review': forms.TextInput(attrs={'class':'form-control', 'placeholder':'Review'}),
        }