from django.shortcuts import render


def page_not_found_view(request, exception):
    return render(request, "main/404.html", status=404)


def custom_error_view(request, exception=None):
    return render(request, "main/500.html", status=500)

