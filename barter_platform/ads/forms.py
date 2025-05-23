from django import forms
from .models import Ad, ExchangeProposal
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError

class AdForm(forms.ModelForm):
    description = forms.CharField(
        widget=forms.Textarea(
            attrs={
                'class':      'form-control',
                'rows':       4,              
                'placeholder':'Describe your item…'
            }
        )
    )
    class Meta:
        model = Ad
        fields = ['title', 'description', 'image_url', 'category', 'condition']
        widgets =  widgets = {
            'title':     forms.TextInput(attrs={'class':'form-control'}),
            'image_url': forms.URLInput( attrs={'class':'form-control'}),
            'category':  forms.TextInput(attrs={'class':'form-control'}),
            'condition': forms.Select(   attrs={'class':'form-select'}),
        }


class ExchangeProposalForm(forms.ModelForm):
    comment = forms.CharField(
        widget=forms.Textarea(
            attrs={
                'class':      'form-control',
                'rows':       4,              
                'placeholder':'comment…'
            }
        )
    )
    class Meta:
        model = ExchangeProposal
        fields = ['ad_sender', 'ad_receiver', 'comment']
        widgets =  widgets = {
            'ad_sender':  forms.Select(   attrs={'class':'form-select'}),
            'ad_receiver': forms.Select(   attrs={'class':'form-select'}),
        }
    def clean(self):
        cleaned = super().clean()
        sender   = cleaned.get('ad_sender')
        receiver = cleaned.get('ad_receiver')

        if sender and receiver:
            exists = exists = ExchangeProposal.objects.filter(
            ad_sender=sender,
            ad_receiver=receiver
            ).exclude(status='rejected').exists()
            if exists:
                raise ValidationError(
                    "You’ve already sent an exchange proposal for this same pair of ads."
                )
        return cleaned

class SignUpForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')
        help_texts = { 
            "username": None, 
            "email": None,
            "password1": None,
            "password2": None,
        }
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.fields["username"].widget.attrs.update({
                "class":"form-control", "placeholder":"Username"
            })
            self.fields["email"].widget.attrs.update({
                "class":"form-control", "placeholder":"Email"
            })
            self.fields["password1"].widget.attrs.update({
                "class":"form-control", "placeholder":"Password"
            })
            self.fields["password2"].widget.attrs.update({
                "class":"form-control", "placeholder":"Confirm password"
            })
