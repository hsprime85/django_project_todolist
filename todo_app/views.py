from django.contrib import messages
from django.shortcuts import render, redirect
import bcrypt
from .models import *


def index(request):
    return render(request, 'index.html')


def register(request):
    return render(request, 'register.html')


def login(request):
    return render(request, 'login.html')


def create_user(request):
    print(request.POST)
    errors = User.objects.register_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/register')
    else:
        print('registering a user')
        password = request.POST['register_password']
        pw_hs = bcrypt.hashpw(
            password.encode(), bcrypt.gensalt()).decode()
        print('password: ', password)
        print('pw_hs: ', pw_hs)

        user = User.objects.create(
            first_name=request.POST['register_first_name'],
            last_name=request.POST['register_last_name'],
            email=request.POST['register_email'],
            password=pw_hs
        )
        request.session['user_id'] = user.id
        return redirect('/current')


def login_user(request):
    errors = User.objects.login_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/login')
    else:
        user_to_login = User.objects.get(
            email=request.POST['login_email']
        )
        request.session['user_id'] = user_to_login.id
        return redirect('/current')


def logout(request):
    request.session.flush()
    return redirect('/')


def current(request):
    if 'user_id' not in request.session:
        return redirect('/')
    else:
        user = User.objects.get(id=request.session['user_id'])
        context = {
            'user': user,
            'uncompleted_todos': Todo.objects.filter(is_completed=False, user=user).order_by('-created_at')
        }
        return render(request, 'current.html', context)


def new_todo(request):
    if 'user_id' not in request.session:
        return redirect('/')
    else:
        user = User.objects.get(id=request.session['user_id'])
        context = {
            'user': user
        }
    return render(request, 'newtodo.html', context)


def create_todo(request):
    if 'user_id' not in request.session:
        return redirect('/')
    else:
        user = User.objects.get(id=request.session['user_id'])
        new_todo = Todo.objects.create(
            title=request.POST['title'],
            memo=request.POST['memo'],
            user=user
        )
        return redirect('/current')


def todo_detail(request, todo_id):
    if 'user_id' not in request.session:
        return redirect('/')
    else:
        user_login = User.objects.get(id=request.session['user_id'])
        context = {
            'todo': Todo.objects.get(id=todo_id),
            'user': user_login,
            'all_todos': Todo.objects.all()
        }
        return render(request, 'detail.html', context)


def todo_update(request, todo_id):
    todo = Todo.objects.get(id=todo_id)
    todo.title = request.POST['title']
    todo.memo = request.POST['memo']
    todo.save()
    return redirect('/current')


def todo_delete(request, todo_id):
    Todo.objects.get(id=todo_id).delete()
    return redirect('/current')


def todo_complete(request, todo_id):
    todo_to_complete = Todo.objects.get(id=todo_id)
    todo_to_complete.is_completed = True
    todo_to_complete.save()
    return redirect('/completed')


def completed(request):
    if 'user_id' not in request.session:
        return redirect('/')
    else:
        user = User.objects.get(id=request.session['user_id'])
        context = {
            'user': user,
            'all_completed_todos': Todo.objects.filter(is_completed=True).filter(user=user).order_by('-updated_at')
        }
        return render(request, 'complete.html', context)
