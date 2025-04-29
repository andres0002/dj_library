# django
from django.shortcuts import render
# from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView
# third
# own
from apps.user.mixins import LoginUserIssuperuserOrIsstaffOrIsactiveRequiredMixin

# Create your views here.

class Home(LoginUserIssuperuserOrIsstaffOrIsactiveRequiredMixin, TemplateView):
    template_name = 'index.html'