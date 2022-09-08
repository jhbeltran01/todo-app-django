from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse
from .models import User, Todo

def index(request):
  return render(request, 'todo/index.html')



def home(request, user_id): 
  user = User.objects.get(pk=user_id)
  todo_list = user.todo_set.all().order_by('id')
  
  
  context = {
    'user': user,
    'todo_list': todo_list,
    'uncompleted_task': len(todo_list.filter(is_completed=False))
  }
  
  return render(request, 'todo/home.html', context)



def credentials_are_incorrect(request):
  username = request.POST['username']
  password = request.POST['password']
  
  context = {
      'log_in_error_message': 'The username or password is incorrect!',
      'username': username,
      'password': password
    }
  
  return render(request, 'todo/index.html', context)



def authenticate_user(request):
  username = request.POST['username']
  password = request.POST['password']
  
  try:
    users = User.objects.get(name=username, password=password)
  except User.DoesNotExist:
    return credentials_are_incorrect(request)
  
  return HttpResponseRedirect(reverse('todo:home', args=(users.id,)))



def create_account(request):  
  return render(request, 'todo/create-account.html')



def save_account(request):
  username = request.POST['username']
  password = request.POST['password']
  
  try:
    User.objects.get(name=username)
  except User.DoesNotExist:
    new_user = User(name=username, password=password)
    new_user.save()
    
    return HttpResponseRedirect(reverse('todo:home', args=(new_user.id,)))

  context = {
    'username_error_message': 'Username already existed!',
    'to_create_account': True,
    'username': username,
    'password': password
  }
  return render(request, 'todo/create-account.html', context)



def create_todo(request, user_id):
  task =  request.POST['todoText'].lower()
  user = User.objects.get(pk=user_id)
  todo_list = user.todo_set.all()
  task_is_on_the_list = len(todo_list.filter(text=task)) >= 1
  
  context = {
      'user': user,
      'todo_list': todo_list,
      'uncompleted_task': len([not todo.is_completed for todo in todo_list]),
    }
  
  if task_is_on_the_list:
    context['todo_error_message'] = 'Task is already on the list!'
    return render(request, 'todo/home.html', context)
  else:
    new_task = user.todo_set.create(text=task)
    new_task.save()
    
    return HttpResponseRedirect(reverse('todo:home', args=(user_id,)))



def delete_task(request, user_id, task_id):
  user = User.objects.get(pk=user_id)
  task_list = user.todo_set.get(pk=task_id)
  task_list.delete()
  
  return HttpResponseRedirect(reverse('todo:home', args=(user_id,)))



def mark_as_completed(request, user_id, task_id):
  user = User.objects.get(pk=user_id)
  task = user.todo_set.get(pk=task_id)
  task.is_completed = not task.is_completed
  task.save() 
  
  return HttpResponseRedirect(reverse('todo:home', args=(user_id,)))



def delete_completed(request, user_id):
  user = User.objects.get(pk=user_id)
  try:
    completed_task = user.todo_set.filter(is_completed=True)
  except (KeyError, Todo.DoesNotExist):
    return HttpResponseRedirect(reverse('todo:home', args=(user_id,)))
  
  completed_task.delete()
  
  return HttpResponseRedirect(reverse('todo:home', args=(user_id,)))



def filter(request, user_id, filter_name):
  user = User.objects.get(pk=user_id)
  is_completed_only = filter_name == 'completed'
  todo_list = user.todo_set.filter(is_completed=is_completed_only).order_by('id')
  active_task = user.todo_set.filter(is_completed=False)
  
  context = {
    'user': user,
    'todo_list': todo_list,
    'uncompleted_task': len(active_task)
  }
  
  return render(request, 'todo/home.html', context)