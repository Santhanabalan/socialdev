from .models import Profile,Skill
from django.db.models import Q

def searchProfiles(request):
    search = ''
    if request.GET.get('search'):
        search = request.GET.get('search')
    
    skills = Skill.objects.filter(name__icontains=search)
    profiles = Profile.objects.distinct().filter(
        Q(name__icontains=search) |
        Q(short_intro__icontains=search) |
        Q(skill__in=skills))
    return search , profiles