from django.shortcuts import render,redirect
from users.models import Profile
from django.contrib.auth.models import User
from django.contrib.auth import login,authenticate,logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from .forms import CustomUserCreationForm, ProfileForm, SkillForm
from .utils import searchProfiles
# Create your views here.
def loginUser(request):
    page = 'login'
    if request.user.is_authenticated:
        return redirect('profiles')
    if request.method == 'POST':
        username= request.POST['username']
        password= request.POST['password']

        try:
            user=User.objects.get(username=username)
        except:
            messages.error(request,'User Not Found')

        user = authenticate(request,username=username,password=password)

        if user is not None:    
            login(request,user)
            return redirect('profiles')
        else:
            messages.error(request,"Password Incorrect")
    context = {'page':page}
    return render (request,'users/login_register.html',context)

def logoutUser(request):
    logout(request)
    messages.success(request,"Logged out Successfully")
    return render (request,'users/login_register.html')
def profiles(request):
    search , profiles = searchProfiles(request)
    context = {'profiles':profiles,'search':search}
    return render (request,'users/profiles.html',context)

def userProfile(request,pk):
    profile = Profile.objects.get(id=pk)
    topSkills = profile.skill_set.exclude(description__exact="")
    otherSkills = profile.skill_set.filter(description="")
    context = {'profile':profile,'topSkills':topSkills,'otherSkills':otherSkills}
    return render (request,'users/user-profile.html',context)

def registerUser(request):
    page='register'
    form = CustomUserCreationForm()
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()

            messages.success(request,"User Created Successfully")
            login(request,user)
            return redirect('edit-account')
        else:
            messages.error(request,"Error during registration")
    context = {'page':page,'form':form}
    return render (request,'users/login_register.html',context)

@login_required(login_url="login")
def userAccount(request):
    profile = request.user.profile
    skills = profile.skill_set.all()
    projects = profile.project_set.all()
    context = {'profile':profile,'skills':skills,'projects':projects}
    return render (request,'users/account.html',context)

@login_required(login_url="login")
def editAccount(request):
    profile = request.user.profile
    form = ProfileForm(instance=profile)
    if request.method == 'POST':
        form = ProfileForm(request.POST,request.FILES,instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request,"Account was edited Successfully")
            return redirect('account')

    context = {'form':form}
    return render (request,'users/profile_form.html',context)

@login_required(login_url="login")
def createSkill(request):
    profile = request.user.profile
    form = SkillForm()
    if request.method == "POST":
        form = SkillForm(request.POST)
        if form.is_valid():
            skill =form.save(commit=False)
            skill.owner = profile
            skill.save()
            messages.success(request,"Skill Created Successfully")
            return redirect('account')
    context={'form':form}
    return render (request,'users/skill_form.html',context)

@login_required(login_url="login")
def updateSkill(request,pk):
    profile = request.user.profile
    skill = profile.skill_set.get(id=pk)
    form = SkillForm(instance=skill)
    if request.method == "POST":
        form = SkillForm(request.POST,instance=skill)
        if form.is_valid():
            form.save()
            messages.success(request,"Skill was Edited Successfully")
            return redirect('account')
    context={'form':form}
    return render (request,'users/skill_form.html',context)

@login_required(login_url="login")
def deleteSkill(request,pk):
    profile = request.user.profile
    skill = profile.skill_set.get(id=pk)
    if request.method == 'POST':
        skill.delete()
        messages.success(request,"Skill was Deleted Successfully")
        return redirect ('account')
    context={'object':skill}
    return render(request,'delete-object.html',context)

