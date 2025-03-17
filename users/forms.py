# users/forms.py
from django import forms
from .models import CustomUser  # Import your custom user model


class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput, required=True)
    confirm_password = forms.CharField(widget=forms.PasswordInput, required=True)

    # Add any necessary fields
    role = forms.ChoiceField(choices=[('student', 'Student'), ('vendor', 'Vendor')], required=True)
    email = forms.EmailField(required=True)

    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password', 'confirm_password', 'role']

    def clean(self):
        cleaned_data = super().clean()
        print("Cleaned Data:", cleaned_data)  # Debugging: print cleaned data
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')

        if password != confirm_password:
            raise forms.ValidationError("Passwords do not match.")

        role = cleaned_data.get('role')
        email = cleaned_data.get('email')

        # Ensure role and email are strings
        if not isinstance(role, str):
            raise forms.ValidationError("Role is not a valid string.")
        if not isinstance(email, str):
            raise forms.ValidationError("Email is not a valid string.")

        return cleaned_data