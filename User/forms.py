from django import forms
from Remote_User.models import ClientRegister_Model
from django.contrib.auth.hashers import make_password


class ClientRegister_Form(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(), min_length=6)

    class Meta:
        model = ClientRegister_Model
        fields = ("username", "email", "password", "phoneno", "country", "state", "city", "gender", "address")

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if ClientRegister_Model.objects.filter(email=email).exists():
            raise forms.ValidationError("Email already exists")
        return email

    def save(self, commit=True):
        user = super().save(commit=False)
        user.password = make_password(self.cleaned_data['password'])
        if commit:
            user.save()
        return user