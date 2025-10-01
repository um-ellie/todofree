from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, CreateView, DeleteView, UpdateView
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from .forms import TaskForm
from .models import Task
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

# Create your views here.


class TaskListView(LoginRequiredMixin, ListView):
    model = Task
    template_name = 'todo/dashboard.html'
    context_object_name = 'tasks'
    paginate_by = 10

    def get_queryset(self):
        return Task.objects.filter(user=self.request.user).order_by('is_done', '-priority', 'due_date', '-created_at')


class TaskCreateView(LoginRequiredMixin, CreateView):
    model = Task
    form_class = TaskForm
    template_name = 'todo/task_form.html'
    success_url = reverse_lazy('todo:dashboard')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class TaskUpdateView(UpdateView):
    model = Task
    form_class = TaskForm
    template_name = "todo/task_form.html"

    def get_success_url(self):
        return reverse_lazy("todo:dashboard")

class TaskDeleteView(LoginRequiredMixin, DeleteView):
    model = Task
    template_name = 'todo/task_confirm_delete.html'
    success_url = reverse_lazy('todo:dashboard')

    def get_queryset(self):
        # Ensure users can only delete their own tasks
        return Task.objects.filter(user=self.request.user)


# Toggle task completion status
@login_required
def toggle_done(request, pk):
    task = get_object_or_404(Task, pk=pk, user=request.user)
    task.is_done = not task.is_done
    task.save(update_fields=['is_done', 'updated_at'])
    return redirect('todo:dashboard')
