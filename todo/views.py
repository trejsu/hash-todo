from django.http import HttpResponse


# todo: remove index and add class for home view here
# todo: add annotation to the view to redirect to login if not authenticated (maybe it could be done to the base view?)
# todo: some unit tests?
def index(request):
    username = "username"
    return HttpResponse(f'Hello, {username}')
