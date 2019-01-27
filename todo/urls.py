from django.urls import path

from .views import HomeView, ToggleTaskStatus, SubmitTask

app_name = 'todo'

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('tasks/toggle_status/<int:id>/', ToggleTaskStatus.as_view(), name='toggle-task-status'),
    path('tasks/submit/', SubmitTask.as_view(), name='submit-task')
]
