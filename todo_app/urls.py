from django.urls import path
from . import views
urlpatterns = [
    path('', views.index),
    path('register', views.register),
    path('create/user', views.create_user),
    path('login', views.login),
    path('login/user', views.login_user),
    path('logout', views.logout),
    path('current', views.current),
    path('newtodo', views.new_todo),
    path('create/todo', views.create_todo),
    path('completed', views.completed),
    path('todo/<int:todo_id>/detail', views.todo_detail),
    path('todo/<int:todo_id>/update', views.todo_update),
    path('todo/<int:todo_id>/delete', views.todo_delete),
    path('todo/<int:todo_id>/complete', views.todo_complete),

]
