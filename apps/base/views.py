# django
from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView

# Create your views here.

class Home(LoginRequiredMixin, TemplateView):
    template_name = 'index.html'