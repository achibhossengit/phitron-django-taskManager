from django.db import models

# Create your models here.

class Employee(models.Model):
    name = models.CharField(max_length=50)
    email = models.EmailField(unique=True)
    # task_set : reverse relations
    # tasks = its changed by related_name = 

class Task(models.Model):
    project = models.ForeignKey(
        "project", 
        on_delete=models.CASCADE,
        default=1,
        related_name="tasks"
    )
    assigned_to = models.ManyToManyField(Employee, related_name="tasks")
    title = models.CharField(max_length=250)
    description = models.TextField()
    due_date = models.DateField()
    is_completed = models.BooleanField(default=False)
    created_at  = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    # taskdetail = reverse relations
    # details = its changed by related_name = 


# one to one
# many to one
# many to many

class TaskDetail(models.Model):
    HIGH = 'H'
    MEDIUM = 'M'
    LOW = 'L'
    PRIORITY_OPTIONS = (
        (HIGH, 'High'),
        (MEDIUM, 'Medium'),
        (LOW, 'Low')
    )
    task = models.OneToOneField(
        Task, 
        on_delete=models.CASCADE,
        related_name="details"
    )
    assigned_to = models.CharField(max_length=100)
    priority = models.CharField(max_length=1, choices=PRIORITY_OPTIONS, default = LOW)
    
# Task.objects.get(id=1)
# select * from task where id=2
# ORM = Object Relational Maper


class Project(models.Model):
    name = models.CharField(max_length=100, default="Untitled")
    start_date = models.DateField(auto_now=True)
    # tasks_set : reverse relations
    # tasks : changed by related name
