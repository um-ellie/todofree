import json
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, CreateView, DeleteView, UpdateView
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from .forms import TaskForm
from .models import Task, Category
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views import View
from django.http import JsonResponse
from django.db.models import Case, When, IntegerField

# Create your views here.


class TaskListView(LoginRequiredMixin, ListView):
    model = Task
    template_name = 'todo/dashboard.html'
    context_object_name = 'tasks'
    paginate_by = 10

    def get_queryset(self):
        # Annotate each task with an integer priority_order for sorting
        return Task.objects.filter(user=self.request.user).annotate(
            priority_order=Case(
                When(priority='L', then=1),
                When(priority='M', then=2),
                When(priority='H', then=3),
                output_field=IntegerField(),
            )
        ).order_by('is_done', '-priority_order', 'due_date', '-created_at')

class TaskCreateView(LoginRequiredMixin, CreateView):
    model = Task
    form_class = TaskForm
    template_name = 'todo/task_form.html'
    success_url = reverse_lazy('todo:dashboard')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user   # Pass the user to the form
        return kwargs
    
    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class TaskUpdateView(UpdateView):
    model = Task
    form_class = TaskForm
    template_name = "todo/task_form.html"

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user   # Pass the user to the form
        return kwargs
    def get_success_url(self):
        return reverse_lazy("todo:dashboard")

class TaskDeleteView(LoginRequiredMixin, DeleteView):
    model = Task
    template_name = 'todo/task_confirm_delete.html'
    success_url = reverse_lazy('todo:dashboard')

    def get_queryset(self):
        # Ensure users can only delete their own tasks
        return Task.objects.filter(user=self.request.user)


class ToggleDoneView(LoginRequiredMixin, View):
    def post(self, request, pk, *args, **kwargs):
        task = get_object_or_404(Task, pk=pk, user=request.user)
        task.is_done = not task.is_done
        task.save(update_fields=['is_done', 'updated_at'])
        return JsonResponse({
            "success": True,
            "task_id": task.pk,
            "is_done": task.is_done
        })

class TaskDeleteAjaxView(LoginRequiredMixin, View):
    def post(self, request, pk, *args, **kwargs):
        task = get_object_or_404(Task, pk=pk, user=request.user)
        task.delete()
        return JsonResponse({
            "success": True,
            "task_id": pk
        })


class AddCategoryAjaxView(LoginRequiredMixin, View):
    def post(self, request):
        data = json.loads(request.body)
        name = data.get('name')
        if name:
            cat = Category.objects.create(user=request.user, name=name)
            return JsonResponse({"success": True, "pk": cat.pk, "name": cat.name})
        return JsonResponse({"success": False})

class DeleteCategoryAjaxView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        data = json.loads(request.body)
        cat_id = data.get('id')
        category = Category.objects.filter(pk=cat_id, user=request.user).first()
        if not category:
            return JsonResponse({'success': False, 'error': 'Category not found'})
        if category.task_set.exists():
            return JsonResponse({'success': False, 'error': 'Category has tasks'})
        category.delete()
        return JsonResponse({'success': True})