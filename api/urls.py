from django.conf.urls import url
from django.urls import path

from .views import AllTasksView, TaskView

urlpatterns = [
    path('tasks/', AllTasksView.as_view(), name="all-tasks"),
    url(r'^tasks/(?P<pk>\d+)/$', TaskView.as_view(), name='task')
]
