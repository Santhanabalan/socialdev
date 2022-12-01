from django.http import JsonResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from projects.models import Project
from .serializer import ProjectSerializer

@api_view(['GET'])
def getRoutes(request):

    route = [
        {'GET':'api/projects'},
        {'GET':'api/projects/id'},
        {'POST':'api/projects/vote'},

        {'POST':'api/users/token'},
        {'POST':'api/users/token/refresh'},
    ]

    return Response(route)

@api_view(['GET'])
def getProjects(request):
    projects = Project.objects.all()
    serializer = ProjectSerializer(projects,many=True)
    return Response(serializer.data)

@api_view(['GET'])
def getProject(request,pk):
    project = Project.objects.get(id=pk)
    serializer = ProjectSerializer(project,many=False)
    return Response(serializer.data)