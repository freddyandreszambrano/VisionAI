from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from .forms import LoginForm, CustomUserCreationForm, EditProfileForm
from django.contrib import messages

def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            # Aquí puedes procesar el formulario de inicio de sesión
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('Main:Main_list')
            else:
                # Si la autenticación falla, agregar un error al formulario
                 messages.error(request, 'Nombre de usuario o contraseña incorrectos.')
    else:
        form = LoginForm()
         
    # Si llega a este punto, significa que no se ha iniciado sesión o que el formulario no es válido
    # Por lo tanto, redirigir de nuevo a la página de inicio de sesión
    return render(request, 'Base_account/login.html', {'form': form})


def register(request):
    data = {'form': CustomUserCreationForm()}
    
    if request.method == 'POST':
        user_create_form = CustomUserCreationForm(data=request.POST)
        
        if user_create_form.is_valid():
            username = user_create_form.cleaned_data['username']

            if User.objects.filter(username=username).exists():
                messages.error(request, 'El nombre de usuario ya está en uso.')
            else:
                password1 = user_create_form.cleaned_data['password1']
                password2 = user_create_form.cleaned_data['password2']
                
                if password1 != password2:
                    messages.error(request, 'Las contraseñas no coinciden.')
                else:
                    user = user_create_form.save(commit=False)
                    user.is_active = True
                    user.is_staff = False
                    user.is_superuser = False
                    user.save()
                    
                    user = authenticate(username=username, password=password1)
                    if user is not None:
                        login(request, user)
                    
                    return redirect('Main:Main_list')
        else:
            for error in user_create_form.errors.values():
                messages.error(request, error)
    else:
        data['form'] = CustomUserCreationForm()
    
    return render(request, 'Base_account/registro.html', data)



def logout_request(request):
    logout(request)
    return redirect('Account:login')



@login_required
def edit_profile(request):
    user = request.user  # Obtener el usuario actualmente autenticado
    if request.method == 'POST':
        form = EditProfileForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.instance)  # Mantener la sesión activa después de cambiar la contraseña
            return redirect('Main:Main_list')
    else:
        form = EditProfileForm(instance=user)
    
    return render(request, 'Edit_profile/edit_profile.html', {'form': form})