from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class ClientRegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True, label="Adresse Email")
    first_name = forms.CharField(max_length=150, required=True, label="Nom de l'Entreprise ou du Navire")
    last_name = forms.CharField(max_length=150, required=True, label="Nom du Contact / Représentant")

    class Meta:
        model = User
        fields = ("username", "email", "first_name", "last_name")
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({'class': 'form-v2-input'})
        
    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        if commit:
            user.save()
        return user
