from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse
from django.views.generic import ListView, View

from .models import Task


class HomeView(LoginRequiredMixin, ListView):
    template_name = 'todo/home.html'

    def get_queryset(self):
        return Task.objects.filter(user=self.request.user)


class ToggleTaskStatus(View):
    def get(self, request, id):
        task = get_object_or_404(Task, pk=id)
        status = task.opposite_status()
        task.status = status
        task.save()
        return redirect(reverse("todo:home"))
