from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib import messages
from django.contrib.auth.models import User

# Create your views here.
def show_Base_account_page(request):
    return render(request, 'Base_account/Base_account.html')# test_login.py

# def registro(request):
#     if request.method == "POST":
#         form = UserCreationForm(request.POST)
#         if form.is_valid():
#             form.save()
#             return redirect('Account:login')
#     else:
#         form = UserCreationForm()
#     return render(request, 'Base_account/registro.html', {"form": form})


def registro(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            # Verificar si el usuario ya existe
            if User.objects.filter(username=username).exists():
                messages.error(request, "Este usuario ya está registrado.")
            else:
                form.save()
                # Autenticar al usuario recién registrado
                user = authenticate(username=username, password=raw_password)
                login(request, user)
                messages.success(request, "Tu cuenta ha sido creada exitosamente. ¡Bienvenido!")
                return redirect('Main:main_view')
    else:
        form = UserCreationForm()
    return render(request, 'Base_account/registro.html', {"form": form})


def login_request(request):
    if request.method == "POST":
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            return redirect('Main:main_view')
            if user is not None:
                login(request, user)
                return redirect('Account:registro')
    
    form = AuthenticationForm()
    return render(request, 'Base_account/login.html', {"form": form})
    
def logout_request(request):
    logout(request)
    return redirect('Account:login')



