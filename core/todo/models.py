from django.db import models
from django.conf import settings
from django.utils import timezone

# Priority choices for tasks
class Priority(models.TextChoices):
    LOW = 'L', 'Low'
    MEDIUM = 'M', 'Medium'
    HIGH = 'H', 'High'


class Category(models.Model):
    """
    Model for task categories. Each user can have multiple categories.
    """
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='categories'
    )
    name = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'name')
        ordering = ['name']
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.name


class Task(models.Model):
    """
    Model for tasks in the to-do application.
    Each task is associated with a user and can optionally belong to a category.
    """
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='tasks'
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='tasks'
    )
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    is_done = models.BooleanField(default=False, db_index=True)
    priority = models.CharField(
        max_length=1,
        choices=Priority.choices,
        default=Priority.MEDIUM,
        db_index=True
    )
    due_date = models.DateTimeField(null=True, blank=True, db_index=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['is_done', '-priority', 'due_date', '-created_at']
        indexes = [
            models.Index(fields=['user', 'is_done']),
            models.Index(fields=['due_date']),
        ]

    def mark_done(self):
        """Mark task as done."""
        self.is_done = True
        self.save(update_fields=['is_done', 'updated_at'])

    def is_overdue(self):
        """Check if the task is overdue."""
        return self.due_date and (self.due_date < timezone.now()) and not self.is_done

    def remaining_seconds(self):
        """Return remaining seconds until due date."""
        if not self.due_date:
            return None
        return (self.due_date - timezone.now()).total_seconds()

    def __str__(self):
        return self.title[:50]


class TaskComment(models.Model):
    """
    Model for comments on tasks.
    Each comment is associated with a task and a user.
    """
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['created_at']

    def __str__(self):
        return f"Comment by {self.user.email} on {self.task.title[:20]}"
