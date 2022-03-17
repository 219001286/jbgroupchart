
from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import HttpResponse
from django.db.models import Q
from django.contrib.auth import authenticate, login, logout
from base.models import Department, Message, Topic, User
from .forms import DepartmentForm, UserForm, MyUserCreationForm
from django.contrib.auth.decorators import login_required



# loginUser
def loginPage(request):
    page = 'login'
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        email = request.POST.get('email').lower()
        password = request.POST.get('password')

        try: 
            user = User.objects.get(email=email)
        except:
            messages.error(request, 'user does not exis')

        user = authenticate(request, username=email, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'the email or password intered is not correct')


    context = {'page':page}
    return render (request, 'base/login_register.html', context)

# logoutUser
def logoutUser(request):
    logout(request)
    return redirect('home')

def registerPage(request):
    form = MyUserCreationForm()

    if request.method == 'POST':
        form = MyUserCreationForm(request.POST)
        if form.is_valid():
             user = form.save(commit=False)
             user.username = user.username.lower() 
             user.save()
             login(request, user)
             return redirect('home')
        else:
            messages.error(request, 'An error occurred in the registration')


    context = {'form':form}
    return render (request, 'base/login_register.html', context)

# function for the homepage
def Home(request):
    q=request.GET.get('q') if request.GET.get('q') else ''
    departments = Department.objects.filter(
        Q(topic__name__icontains=q) |
        Q(name__icontains=q) | 
        Q(description__icontains=q)|
        Q()
        )
    department_count = departments.count()
    topics = Topic.objects.all()[0:5]
    room_messages = Message.objects.filter(
        Q(department__topic__name__icontains=q) |
        Q(department__name__icontains=q) |
        Q(department__created__icontains=q) |
        Q(body__icontains=q)
        )
    context = {'department':departments, 'topics':topics, 'department_count':department_count, 'room_messages':room_messages}
    return render(request, 'base/home.html' , context)

# function to the room page
def Room(request, pk):
    specific_department = Department.objects.get(id=pk)
    messages = specific_department.message_set.all().order_by('-created')
    participants = specific_department.participants.all()
    if request.method == 'POST':
        message = Message.objects.create(
            user = request.user,
            department = specific_department,
            body = request.POST.get('body')
            )
        specific_department.participants.add(request.user)
   
    context = {'department':specific_department, 'department_messages':messages,'participants':participants}
    return render(request, 'base/room.html', context)

def userProfile(request,pk):
    user = User.objects.get(id=pk)
    department = user.department_set.all()
    room_messages = user.message_set.all()
    topics = Topic.objects.all()
    context = {'user':user, 'department':department, 'room_messages': room_messages, 'topics':topics}
    return render(request, 'base/profile.html', context)

# the view of the department creation
@login_required(login_url='login') 
def createDepartment(request):
    form = DepartmentForm()
    topics = Topic.objects.all()
    if request.method == 'POST':
        topic_name = request.POST.get('topic')
        topic, created = Topic.objects.get_or_create(name=topic_name)

        Department.objects.create(
            host = request.user,
            topic=topic,
            name=request.POST.get('name'),
            description=request.POST.get('description'),
        )
        return redirect('home')
    

    context = {'form': form, 'topics':topics}
    return render(request, 'base/department_form.html', context)


# updating the room
@login_required(login_url='login')
def UpdateDepartment(request, pk):
    department = Department.objects.get(id=pk)
    form = DepartmentForm(instance=department)
    topics = Topic.objects.all()
    if request.user != department.host:
        return HttpResponse("you are not allowed to edit this room")

    if request.method == 'POST':
        topic_name = request.POST.get('topic')
        topic, created = Topic.objects.get_or_create(name=topic_name)
        department.name = request.POST.get('name')
        department.topic=topic
        department.description=request.POST.get('description')
        department.save()
        return redirect('home')
    context = {'form':form, 'topics':topics, 'department':department}
    return render (request, 'base/department_form.html', context) 
 

# Deleting the department
@login_required(login_url='login')
def deleteDepartment(request, pk):
    department = Department.objects.get(id=pk)
 
    if request.user != department.host:
        return HttpResponse("you are not allowed to edit this room")
        
    if request.method == 'POST':
        department.delete()
        return redirect('home')
    return render(request, 'base/delete.html', {'obj':department})
    

# Deleting a particular message
@login_required(login_url='login')
def deleteMessage(request, pk):
    message = Message.objects.get(id=pk)
        
    if request.method == 'POST':
        message.delete()
        return redirect('home')
    return render(request, 'base/delete.html', {'obj':message})



# the function to edit a user profile
@login_required(login_url='login')
def UpdateUser(request): 
    user = request.user
    form = UserForm(instance=user)

    if request.method == 'POST':
        form = UserForm(request.POST,request.FILES, instance=user)
        if form.is_valid():
            form.save()
            return redirect('user_profile', pk=user.id)
    context = {'form':form}
    return render(request, 'base/edit-user.html', context)


def TopicPage(request):
    q=request.GET.get('q') if request.GET.get('q') else ''
    topics = Topic.objects.filter(name__icontains=q)
    context = {'topics':topics}
    return render(request, 'base/topics.html', context)


def Activity(request):
    room_messages = Message.objects.all()
    context = {'room_messages':room_messages}
    return render (request, 'base/activity.html',context)