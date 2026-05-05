from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User
from services.models import Service


class RegisterForm(UserCreationForm):
    services = forms.ModelMultipleChoiceField(
        queryset=Service.objects.all(),
        required=False,
        widget=forms.CheckboxSelectMultiple
    )

    aadhar_card = forms.ImageField(required=False)
    passport_photo = forms.ImageField(required=False)
    cv = forms.FileField(required=False)
    driving_license = forms.ImageField(required=False)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2', 'role']

    # 🔥 CUSTOM VALIDATION
    def clean(self):
        cleaned_data = super().clean()
        role = cleaned_data.get('role')

        if role == 'provider':
            if not cleaned_data.get('aadhar_card'):
                raise forms.ValidationError("Aadhar card is required for provider registration.")

            if not cleaned_data.get('passport_photo'):
                raise forms.ValidationError("Passport photo is required.")

            if not cleaned_data.get('cv'):
                raise forms.ValidationError("CV is required.")

            if not cleaned_data.get('driving_license'):
                raise forms.ValidationError("Driving license is required.")

            if not cleaned_data.get('services'):
                raise forms.ValidationError("Please select at least one service.")

        return cleaned_data