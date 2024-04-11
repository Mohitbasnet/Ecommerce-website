from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from . models import Contact
from .models import CustomUser
from django import forms
from django.core.validators import RegexValidator
from django import forms
class CustomUserCreationForm(UserCreationForm):

    class Meta(UserCreationForm):
        model = CustomUser
        fields = ('email',)


class CustomUserChangeForm(UserChangeForm):

    class Meta:
        model = CustomUser
        fields = ('email',)

class ContactUsForm(forms.ModelForm):
    # email = forms.EmailField(required=True)
    # name = forms.CharField(max_length=5, required=True)
    
    # phone_regex = RegexValidator( regex = r'^\d{10}$',message = "phone number should exactly be in 10 digits")
    # phone = forms.CharField(max_length=255, required=True, validators=[phone_regex])
    # query = forms.CharField(widget = forms.Textarea)
    class Meta:
        model = Contact
        fields = [
            'email',
            'phone',
            'query',
            'name'
        ]