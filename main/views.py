from django.shortcuts import render, redirect, HttpResponse
from django.views.generic import TemplateView
# Create your views here.

class HomeView(TemplateView):
    
    template_name = 'app_main/index.html'

    def get(self, request, *args, **kwargs):

        return render(request, self.template_name)