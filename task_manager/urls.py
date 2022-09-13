from django.contrib import admin
from django.urls import path

from . import views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name='index'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    # Users
    path('users/create/', views.signup, name='signup'),
    path('users/', views.users, name='users'),
    path('users/<int:user_id>/update/', views.user_update, name='user_update'),
    path('users/<int:user_id>/delete/', views.user_delete, name='user_delete'),
    # Tasks
    path('tasks/', views.tasks, name='tasks'),
    path('tasks/create/', views.task_create, name='task_create'),
    path('tasks/<int:task_id>/', views.task_detail, name='task_detail'),
    path('tasks/<int:task_id>/update/', views.task_update, name='task_update'),
    path('tasks/<int:task_id>/delete/', views.task_delete, name='task_delete'),
    # Statuses
    path('statuses/', views.statuses, name='statuses'),
    path('statuses/create/', views.status_create, name='status_create'),
    path('statuses/<int:status_id>/update/', views.status_update, name='status_update'),
    path('statuses/<int:status_id>/delete/', views.status_delete, name='status_delete'),
    # Labels
    path('labels/', views.labels, name='labels'),
    path('labels/create/', views.label_create, name='label_create'),
    path('labels/<int:label_id>/update/', views.label_update, name='label_update'),
    path('labels/<int:label_id>/delete/', views.label_delete, name='label_delete'),
]
