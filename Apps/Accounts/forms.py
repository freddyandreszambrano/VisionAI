from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, PasswordChangeForm
from django.contrib.auth.models import User

#Inicio De Sesion
class LoginForm(forms.Form):
    username = forms.CharField(label='Nombre de Usuario:', max_length=100)
    password = forms.CharField(label='Contraseña:', widget=forms.PasswordInput)


#Crear Nuevo Perfil
class CustomUserCreationForm(UserCreationForm):
    # is_active = forms.BooleanField(required=False, initial=True)
    # is_staff = forms.BooleanField(required=False, initial=True)
    # is_superuser = forms.BooleanField(required=False, initial=False)
    username = forms.CharField(label='Nombre de Usuario')
    password1 = forms.CharField(label='Contraseña:', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Confirmar Contraseña:', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2')
        labels = {
            'username': 'Nombre de Usuario:',
            'first_name': 'Nombre:',
            'last_name': 'Apellido:',
            'email': 'Correo Electrónico:',
        }

#Editar Perfil
class EditProfileForm(UserChangeForm):
    password1 = forms.CharField(
        label='Nueva Contraseña:',
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
        required=False
    )
    password2 = forms.CharField(
        label='Confirmar Nueva Contraseña:',
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
        required=False
    )

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2')
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
        }
        labels = {
            'username': 'Nombre de Usuario:',
            'first_name': 'Nombre:',
            'last_name': 'Apellido:',
            'email': 'Correo Electrónico:',
        }

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password1 and password1 != password2:
            raise forms.ValidationError("Las contraseñas no coinciden.")
        return password2

    def save(self, commit=True):
        user = super(EditProfileForm, self).save(commit=False)
        password = self.cleaned_data.get('password1')
        if password:
            user.set_password(password)
        if commit:
            user.save()
        return user