from .models import Project,Tag
from django.db.models import Q

def searchProjects(request):
    search = ''
    if request.GET.get('search'):
        search = request.GET.get('search')
    
    tags = Tag.objects.filter(name__icontains=search)

    projects = Project.objects.distinct().filter(
        Q(title__icontains=search) |
        Q(description__icontains=search) |
        Q(owner__name__icontains=search) |
        Q(tags__in=tags)
    )
    return projects,search