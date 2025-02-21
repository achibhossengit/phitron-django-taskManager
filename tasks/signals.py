from tasks.models import Task
from django.db.models.signals import post_save, pre_save, m2m_changed
from django.dispatch import receiver
from django.core.mail import send_mail

# signals
# @receiver(post_save, sender=Task)
# def notify_task_creation(sender, instance, created, **kwargs):
#     if created:
#         instance.is_completed=True
#         instance.save() # its update the data not create. That's why created will be false after that
#     print('sender', sender)
#     print('instance', instance)
#     print( kwargs)

# pre-save signals
# @receiver(pre_save, sender=Task)
# def notify_task_creation(sender, instance,  **kwargs):
#     instance.is_completed=True


# signals for email
@receiver(m2m_changed, sender=Task.assigned_to.through)
def notify_employees_on_task_creation(sender, instance, action, **kwargs):
    if action=='post_add':
        emails = [emp.email for emp in instance.assigned_to.all()]
        send_mail(
        "Django sending email testing",
        f"Hello employee, you have been added in a new task.Task Name: {instance.title}",
        "mail.achibhossen@gmail.com",
        emails,
        fail_silently=False,
        )