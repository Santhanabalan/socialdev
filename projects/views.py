from django.shortcuts import render,redirect
from projects.models import Project,Tag
from projects.forms import ProjectForm,ReviewForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from .utils import searchProjects,paginateProjects

# Create your views here.
def projects(request):
    projects,search = searchProjects(request)
    custom_index,projects = paginateProjects(request,projects,6)
    context = {'projects':projects,'search':search,'custom_index':custom_index}
    return render(request,'projects/projects.html',context)

def project(request,pk):
    projectObj = Project.objects.get(id=pk)
    tags = projectObj.tags.all()
    form = ReviewForm()

    if request.method == 'POST':
        form = ReviewForm(request.POST)
        review = form.save(commit=False)
        review.project = projectObj
        review.owner = request.user.profile
        review.save()
        messages.success(request,'Vote Submitted Succefully')
        return redirect('project',pk=projectObj.id)
    context = {'project':projectObj,'tags':tags,'form':form}
    return render(request,'projects/single-project.html',context)

@login_required(login_url="login")
def createProject(request):
    profile = request.user.profile
    form = ProjectForm()
    if request.method == 'POST':
        newtags = request.POST.get('newtags').replace(',', "").split()
        form = ProjectForm(request.POST,request.FILES)
        if form.is_valid():
            project = form.save(commit=False)
            project.owner = profile
            project.save()
            for tag in newtags:
                tag , created = Tag.objects.get_or_create(name=tag)
                project.tags.add(tag)
            return redirect ('account')
    context={'form':form}
    return render(request,'projects/project-form.html',context)

@login_required(login_url="login")
def updateProject(request,pk):
    profile = request.user.profile
    project = profile.project_set.get(id=pk)
    form = ProjectForm(instance=project)
    if request.method == 'POST':
        newtags = request.POST.get('newtags').replace(',', "").split()
        form = ProjectForm(request.POST,request.FILES,instance=project)
        if form.is_valid():
            project = form.save()
            for tag in newtags:
                tag , created = Tag.objects.get_or_create(name=tag)
                project.tags.add(tag)
            return redirect ('account')
    context={'form':form,'project':project}
    return render(request,'projects/project-form.html',context)

@login_required(login_url="login")
def deleteProject(request,pk):
    profile = request.user.profile
    project = profile.projects_set.get(id=pk)
    if request.method == 'POST':
        project.delete()
        return redirect ('account')
    context={'object':project}
    return render(request,'delete-object.html',context)
