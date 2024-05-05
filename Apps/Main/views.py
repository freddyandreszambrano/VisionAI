from django.shortcuts import render

# Create your views here.

def Main_view(request):
    return render(request, 'Home/main.html')