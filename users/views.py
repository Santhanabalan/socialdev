from django.shortcuts import render,redirect
from users.models import Profile
from django.contrib.auth.models import User
from django.contrib.auth import login,authenticate,logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from .forms import CustomUserCreationForm, ProfileForm, SkillForm, MessageForm
from .utils import searchProfiles,paginateProfiles
# Create your views here.
def loginUser(request):
    page = 'login'
    if request.user.is_authenticated:
        return redirect('profiles')
    if request.method == 'POST':
        username= request.POST['username'].lower()
        password= request.POST['password']

        try:
            user=User.objects.get(username=username)
        except:
            messages.error(request,'User Not Found')

        user = authenticate(request,username=username,password=password)

        if user is not None:    
            login(request,user)
            return redirect(request.GET['next'] if 'next' in request.GET else 'account')
        else:
            messages.error(request,"Password Incorrect")
    context = {'page':page}
    return render (request,'users/login_register.html',context)

def logoutUser(request):
    logout(request)
    messages.success(request,"Logged out Successfully")
    return redirect('login')
def profiles(request):
    search , profiles = searchProfiles(request)
    custom_index,profiles = paginateProfiles(request,profiles,6)
    context = {'profiles':profiles,'search':search,'custom_index':custom_index}
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
            username = user.username.lower()
            if User.objects.filter(username = username).first():
                messages.error(request, "This username is already taken")
                return redirect('login')
            user.username = username
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

@login_required(login_url="login")
def inbox(request):
    profile = request.user.profile
    messageRequests = profile.messages.all()
    unreadCount = messageRequests.filter(is_read=False).count()
    context = {'messageRequests':messageRequests,'unreadCount':unreadCount}
    return render (request,'users/inbox.html',context)

@login_required(login_url="login")
def viewMessage(request,pk):
    profile = request.user.profile
    message = profile.messages.get(id=pk)
    if message.is_read == False:
        message.is_read = True
        message.save()
    context = {'message':message}
    return render (request,'users/message.html',context)

def sendMessage(request,pk):
    recipient = Profile.objects.get(id=pk)
    form = MessageForm()

    try:
        sender = request.user.profile
    except:
        sender = None

    if request.method == "POST":
        form = MessageForm(request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            message.sender = sender
            message.recipient = recipient

            if sender:
                message.name = sender.name 
                message.email = sender.email
            message.save() 

            messages.success(request,"Message sent successfully")
            return redirect('user-profile',pk=recipient.id)
    context = {'recipient':recipient,'form':form}
    return render (request,'users/message_form.html',context)