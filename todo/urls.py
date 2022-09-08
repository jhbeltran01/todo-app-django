from django.urls import path
from . import views

app_name = 'todo'

urlpatterns = [
    path('', views.index, name='index'),
    path('<int:user_id>/home/', views.home, name='home'),
    path('authenticate-user/', views.authenticate_user, name='authenticate'),
    path('create-account/', views.create_account, name='create-account'),
    path('save-account/', views.save_account, name='save-account'),
    path('<int:user_id>/create-todo/', views.create_todo, name='create-todo'),
    path('<int:user_id>/<int:task_id>/delete/', views.delete_task, name='delete-task'),
    path('<int:user_id>/<int:task_id>/completed', views.mark_as_completed, name='completed'),
    path('<int:user_id>/delete-completed/', views.delete_completed, name='delete-completed'),
    path('<int:user_id>/<str:filter_name>/active-task/', views.filter, name='filter')
]
