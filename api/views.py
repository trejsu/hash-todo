from rest_framework import generics
from rest_framework.filters import OrderingFilter

from api.serializers import TaskSerializer
from todo.models import Task


class AllTasksView(generics.ListCreateAPIView):
    serializer_class = TaskSerializer
    filter_backends = (OrderingFilter,)
    ordering_fields = ('text', 'date')
    ordering = ('date', 'text')

    def get_queryset(self):
        return Task.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class TaskView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = TaskSerializer

    def get_queryset(self):
        return Task.objects.filter(user=self.request.user)
