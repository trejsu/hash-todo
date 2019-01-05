from django.urls import path
from django.views.generic.base import TemplateView

app_name = 'todo'

urlpatterns = [
    path('', TemplateView.as_view(template_name='todo/home.html'), name='home')
]
