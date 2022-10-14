from multiprocessing import context
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from .forms import CrearTaks
from .models import Task
from django.utils import timezone
from django.contrib.auth.decorators import login_required

# Create your views here.

def home(request):
    return render(request,'home.html')

def signup(request):
    if request.method == 'GET':
        return render(request,'signup.html', {
        'form': UserCreationForm  })
    
    else:
        if request.POST['password1'] == request.POST['password2']:
            # register user
            try:
                user = User.objects.create_user(username=request.POST['username'], password=request.POST['password2'])
                user.save()
                login(request, user)
                return redirect('tasks')
               
            except:
                 return render(request,'signup.html', {
        'form': UserCreationForm, 
        'error': 'el usuario ya existe' })


        else:    
             return render(request,'signup.html', {
        'form': UserCreationForm, 
        'error': 'Contraseña no coinciden' })

@login_required
def tasks(request):
    task = Task.objects.filter(user=request.user, datecompleted__isnull=True)

    context = {
        'task': task
    }
    return render(request,'tasks.html', context) 

@login_required
def tasks_complete(request):
    task = Task.objects.filter(user=request.user, datecompleted__isnull=False)

    context = {
        'task': task
    }
    return render(request,'tasks.html', context)         

@login_required
def task_detail(request, id):
    if request.method == 'GET':
        task = get_object_or_404(Task, pk=id, user=request.user)
        form = CrearTaks(instance=task)
        context = {'task': task,'form': form}
        return render(request,'task_detail.html', context)   
    else:
        try:
            task = get_object_or_404(Task, pk=id, user=request.user)
            form = CrearTaks(request.POST, instance=task)      
            form.save()
            return redirect('tasks')
        except ValueError:
            return render(request,'task_detail.html', {'error': 'Error actualizando la Tarea'})   

@login_required
def complete_task(request, id):
    task = get_object_or_404(Task, pk=id, user=request.user)
    if request.method == 'POST':
        task.datecompleted = timezone.now()
        task.save()
        return redirect('tasks')

@login_required
def delete_task(request, id):
    task = get_object_or_404(Task, pk=id, user=request.user)
    if request.method == 'POST':
        task.delete()
        return redirect('tasks')       

@login_required
def create_task(request):
    if request.method == 'GET':
        return render(request, 'created_task.html',{
        'form': CrearTaks})
    else:
        try:
            form = CrearTaks(request.POST)
            new_task = form.save(commit=False)
            new_task.user = request.user
            new_task.save()
            return redirect('tasks')
        except ValueError:
             return render(request, 'created_task.html',{
             'form': CrearTaks,   
             'error': 'Por favor Proveer Datos Validos'     
         }) 
         
@login_required
def signout(request):
    logout(request)
    return redirect('home')

def signin(request):
    if request.method == 'GET':
        return render(request,'signin.html', {
            'form': AuthenticationForm
        })   
    else:
        user = authenticate(request, username=request.POST['username'], password=request.POST['password'])
        if user is None:
            return render(request, 'signin.html', {
                'form': AuthenticationForm,
                'error': 'Invalid username or password',
            })
        else:
            login(request, user)
            return redirect('tasks')    


    
  

