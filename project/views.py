from django.shortcuts import redirect, render
from django.http import HttpResponse


def home(request):
    return render(request, 'main/home.html', {})
