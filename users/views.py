
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.views.decorators.cache import never_cache

def home_view(request):
    return render(request, 'home.html')

def signup_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # Iniciar sesión automáticamente tras el registro
            return redirect('inbox')  # Redirigir a la bandeja de entrada
    else:
        form = UserCreationForm() # Carga un formulario vacío para solicitudes GET
    return render(request, 'login/signup.html', {'form': form})

@never_cache
def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)  # Iniciar sesión
            return redirect('inbox')  # Redirigir a la bandeja de entrada
    else:
        form = AuthenticationForm()
    return render(request, 'login/login.html', {'form': form})

@never_cache
def logout_view(request):
    if request.method == 'POST': 
        logout(request)
        return redirect('login')  # Redirigir al login tras cerrar sesión
    return redirect('inbox')  # Redirige a la bandeja de entrada si el método no es POST