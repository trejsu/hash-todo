from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView

from .models import Task


class HomeView(LoginRequiredMixin, ListView):
    template_name = 'todo/home.html'

    def get_queryset(self):
        return Task.objects.filter(user=self.request.user)
