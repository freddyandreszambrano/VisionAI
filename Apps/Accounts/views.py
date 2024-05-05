from django.shortcuts import render
# Create your views here.
def show_login_page(request):
    return render(request, 'Login/Login.html')# test_login.py
    