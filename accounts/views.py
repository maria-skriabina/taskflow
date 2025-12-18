from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from .forms import RegistrationForm, ProfileForm

User = get_user_model()

# Регистрация
def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Регистрация прошла успешно!')
            return redirect('accounts:profile')
    else:
        form = RegistrationForm()
    
    return render(request, 'accounts/register.html', {'form': form})

# Логин
class CustomLoginView(LoginView):
    template_name = 'accounts/login.html'
    redirect_authenticated_user = True
    
    def get_success_url(self):
        return reverse_lazy('accounts:profile')

# Логаут
class CustomLogoutView(LogoutView):
    next_page = reverse_lazy('accounts:login')

# Профиль
@login_required
def profile(request):
    user = request.user
    
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Профиль успешно обновлен!')
            return redirect('accounts:profile')
    else:
        form = ProfileForm(instance=user)
    
    context = {
        'form': form,
        'user': user,
    }
    return render(request, 'accounts/profile.html', context)
