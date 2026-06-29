from django.urls import path
from . import views

urlpatterns = [

    # Home
    path('', views.home, name='home'),

    # Dashboard
    path('dashboard/', views.dashboard, name='dashboard'),

    # Skill 

    path('skills/', views.skill_list, name='skill_list'),
    path('skills/add/', views.add_skill, name='add_skill'),
    path('skills/edit/<int:id>/', views.edit_skill, name='edit_skill'),
    path('skills/delete/<int:id>/', views.delete_skill, name='delete_skill'),

    #  Topic 

    path('topics/', views.topic_list, name='topic_list'),
    path('topics/add/', views.add_topic, name='add_topic'),
    path('topics/edit/<int:id>/', views.edit_topic, name='edit_topic'),
    path('topics/delete/<int:id>/', views.delete_topic, name='delete_topic'),

    #  Daily Task 

    path('tasks/', views.task_list, name='task_list'),
    path('tasks/add/', views.add_task, name='add_task'),
    path('tasks/edit/<int:id>/', views.edit_task, name='edit_task'),
    path('tasks/delete/<int:id>/', views.delete_task, name='delete_task'),

    #  Study Log 

    path('studylogs/', views.studylog_list, name='studylog_list'),
    path('studylogs/add/', views.add_studylog, name='add_studylog'),
    path('studylogs/edit/<int:id>/', views.edit_studylog, name='edit_studylog'),
    path('studylogs/delete/<int:id>/', views.delete_studylog, name='delete_studylog'),

]