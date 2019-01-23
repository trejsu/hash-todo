from django.conf.urls import url
from django.urls import path

from .views import ListTasksView, TaskView

urlpatterns = [
    path('tasks/', ListTasksView.as_view(), name="get-all-tasks"),
    url(r'^tasks/(?P<pk>\d+)/$', TaskView.as_view(), name='task')
]
