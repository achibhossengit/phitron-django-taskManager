from django.db import models
from django.conf import settings

class Task(models.Model):
    STATUS_OPTIONS = (
        ("PENDING", 'Pending'),
        ("IN_PROGRESS", 'In Progress'),
        ("COMPLETED", 'Completed')
    )
    status = models.CharField(max_length=15, choices=STATUS_OPTIONS, default="PENDING")
    project = models.ForeignKey(
        "project", 
        on_delete=models.CASCADE,
        default=1,
        related_name="tasks"
    )
    assigned_to = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name="tasks", blank=True)
    title = models.CharField(max_length=250)
    description = models.TextField()
    due_date = models.DateField()
    created_at  = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    # taskdetail: reverse relations -> details: changed by related_name

    def __str__(self):
        return self.title

class TaskDetail(models.Model):
    HIGH = 'H'
    MEDIUM = 'M'
    LOW = 'L'
    PRIORITY_OPTIONS = (
        (HIGH, 'High'),
        (MEDIUM, 'Medium'),
        (LOW, 'Low')
    )
    # one to one
    task = models.OneToOneField(
        Task,
        on_delete=models.CASCADE,
        related_name="details"
    )
    priority = models.CharField(max_length=1, choices=PRIORITY_OPTIONS, default = LOW)
    notes = models.TextField(blank=True, null=True)
    asset = models.ImageField(upload_to='tasks_asset', blank=True, null=True, default='tasks_asset/default_img.jpg')

# ORM = Object Relational Maper
# select * from task where id=2 -> Task.objects.get(id=1)
    def __str__(self):
        return f"Details of Task {self.task.title}"


class Project(models.Model):
    name = models.CharField(max_length=100, default="Untitled")
    description = models.CharField(blank=True, null=True)
    start_date = models.DateField(auto_now=True)
    # tasks_set: reverse relations -> tasks

    def __str__(self):
        return self.name