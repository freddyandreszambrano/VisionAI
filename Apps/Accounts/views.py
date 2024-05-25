from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from .forms import LoginForm, CustomUserCreationForm
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

            return redirect('Main:main_view')
    else:
        form = LoginForm()

    return render(request, 'Base_account/login.html', {'form': form})




def register(request):
    data = {'form': CustomUserCreationForm()}

    if request.method == 'POST':
        user_create_form = CustomUserCreationForm(data = request.POST)

        if user_create_form.is_valid():
            user_create_form.save()
            user = authenticate(username=user_create_form.cleaned_data['username'], password=user_create_form.cleaned_data['password1'])
            return redirect('Main:main_view')    

    return render(request, 'Base_account/registro.html', data)

def logout_request(request):
    logout(request)
    return redirect('Account:login')



