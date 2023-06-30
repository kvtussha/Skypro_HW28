from django.http import JsonResponse


def status_view(request):
    response = {"status": "ok"}
    return JsonResponse(response)
