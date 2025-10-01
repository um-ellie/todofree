from django import forms
from .models import Task, Category
class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ["title", "description", "due_date", "priority", "category"]
        widgets = {
            'due_date': forms.DateTimeInput(attrs={'type': 'datetime-local', 'class': 'border rounded px-2 py-1 w-full'}),
            'priority': forms.Select(attrs={'class': 'border rounded px-2 py-1 w-full'}),
            'category': forms.Select(attrs={'class': 'border rounded px-2 py-1 w-full'}),
            'title': forms.TextInput(attrs={'class': 'border rounded px-2 py-1 w-full'}),
            'description': forms.Textarea(attrs={'class': 'border rounded px-2 py-1 w-full', 'rows': 4}),
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if user:

            self.fields['category'].queryset = Category.objects.filter(user=user)
        else:

            self.fields['category'].queryset = Category.objects.none()