from django.urls import path
from . import views

app_name = 'todo'

urlpatterns = [
    path('', views.TaskListView.as_view(), name='dashboard'),
    path('create/', views.TaskCreateView.as_view(), name='task-create'),
    path("update/<int:pk>/", views.TaskUpdateView.as_view(), name="task-update"),
    path('delete/<int:pk>/', views.TaskDeleteView.as_view(), name='task-delete'),
    path('toggle/<int:pk>/', views.toggle_done, name='task-toggle'),
]