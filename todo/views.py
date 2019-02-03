from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, redirect
from django.views.generic import ListView, View
from django.views.generic.edit import FormMixin

from .forms import TaskForm
from .models import Task, STATUS


class HomeView(LoginRequiredMixin, ListView, FormMixin):
    template_name = 'todo/home.html'
    form_class = TaskForm

    def get_queryset(self):
        done = self.request.GET.get('done')
        if done == 'true' or done is None:
            return Task.objects.filter(user=self.request.user)
        else:
            return Task.objects.filter(user=self.request.user, status=STATUS.active)


class ToggleTaskStatus(View):
    def get(self, request, id):
        redirect_url = request.META.get('HTTP_REFERER')
        task = get_object_or_404(Task, pk=id)
        status = task.opposite_status()
        task.status = status
        task.save()
        return redirect(redirect_url)


class SubmitTask(View):
    def post(self, request):
        redirect_url = request.META.get('HTTP_REFERER')
        task = Task.objects.create(
            user=self.request.user,
            text=request.POST['text'],
            date=request.POST['date']
        )
        task.save()
        return redirect(redirect_url)
