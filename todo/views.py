from django.http import HttpResponse


def index(request):
    username = "username"
    return HttpResponse(f'Hello, {username}')
