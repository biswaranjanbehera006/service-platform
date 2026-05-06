from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User
from services.models import Service


class RegisterForm(UserCreationForm):

    # 🔥 SERVICES (PROVIDER)
    services = forms.ModelMultipleChoiceField(
        queryset=Service.objects.all(),
        required=False,
        widget=forms.CheckboxSelectMultiple
    )

    # 🔥 DOCUMENTS
    aadhar_card = forms.ImageField(required=False)
    passport_photo = forms.ImageField(required=False)
    cv = forms.FileField(required=False)
    driving_license = forms.ImageField(required=False)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2', 'role']

        # 🔥 ADD BOOTSTRAP CLASSES
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter your name'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Enter email'}),
            'password1': forms.PasswordInput(attrs={'class': 'form-control'}),
            'password2': forms.PasswordInput(attrs={'class': 'form-control'}),
            'role': forms.Select(attrs={'class': 'form-select'}),
        }

    # 🔥 APPLY BOOTSTRAP TO FILE INPUTS
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['aadhar_card'].widget.attrs.update({'class': 'form-control'})
        self.fields['passport_photo'].widget.attrs.update({'class': 'form-control'})
        self.fields['cv'].widget.attrs.update({'class': 'form-control'})
        self.fields['driving_license'].widget.attrs.update({'class': 'form-control'})

    # 🔥 VALIDATION
    def clean(self):
        cleaned_data = super().clean()
        role = cleaned_data.get('role')

        if role == 'provider':

            if not cleaned_data.get('aadhar_card'):
                raise forms.ValidationError("Aadhar card is required.")

            if not cleaned_data.get('passport_photo'):
                raise forms.ValidationError("Passport photo is required.")

            if not cleaned_data.get('cv'):
                raise forms.ValidationError("CV is required.")

            if not cleaned_data.get('driving_license'):
                raise forms.ValidationError("Driving license is required.")

            if not cleaned_data.get('services'):
                raise forms.ValidationError("Select at least one service.")

        return cleaned_data