from django.shortcuts import render
from django.http import HttpResponse


projectsList = [
    {
        'id': '1',
        'title': 'Ecommerce Website',
        'description': 'A fully functional ecommerce website with cart and payment integration'
    },
    {
        'id': '2',
        'title': 'DevHub',
        'description': 'A developer portfolio and community platform built with Django'
    },
    {
        'id': '3',
        'title': 'Weather App',
        'description': 'A weather forecast app that fetches real time data from an API'
    },
    {
        'id': '4',
        'title': 'Chat Application',
        'description': 'A real time chat app with private messaging and group rooms'
    },
    {
        'id': '5',
        'title': 'Task Manager',
        'description': 'A productivity app to manage daily tasks with priorities and deadlines'
    },
]


def projects(request):
    return render(request, 'projects/projects.html', {'projects': projectsList})

def project(request, pk):
    projectObj = None
    for item in projectsList:
        if item['id'] == pk:
            projectObj = item
    return render(request, 'projects/single-project.html', {'project': projectObj})
