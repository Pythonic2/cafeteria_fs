from django.shortcuts import render
from django.views.generic import CreateView,DeleteView,DeleteView,UpdateView
from .forms import CustomUserCreationForm
from django.urls import reverse_lazy
from django.contrib import messages
from django.contrib.auth.views import LoginView, LogoutView
from .models import CustomUser
from django.utils.translation import gettext_lazy
from django.contrib.auth import logout
from django.shortcuts import redirect
from django.contrib.auth import get_user_model


def logout_view(request):
    logout(request)
    return redirect("login")
User = get_user_model()


class SignUpView(CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'register.html'

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, 'Cadastro realizado com sucesso. Por favor, faça o login.')
        return response

    def form_invalid(self, form):
        messages.error(self.request, 'Erro no cadastro. Por favor, verifique os dados informados.')
        return super().form_invalid(form)



class LoginUsuario(LoginView):
    template_name = 'login.html'

    def form_invalid(self, form):
        username = form.cleaned_data.get('username')
        user_exists = CustomUser.objects.filter(username=username).exists()

        error_messages = {
            'invalid_login': gettext_lazy('Verifique o usuário e a senha e tente novamente.'),
            'inactive': gettext_lazy('Usuário inativo.'),
        }
        
        form.error_messages = error_messages
        return super().form_invalid(form)