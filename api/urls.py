from django.conf.urls import url
from django.urls import path

from .views import ListTasksView, DetailTaskView

urlpatterns = [
    path('tasks/', ListTasksView.as_view(), name="get-all-tasks"),
    url(r'^tasks/(?P<pk>\d+)/$', DetailTaskView.as_view(), name='get-task')
]
