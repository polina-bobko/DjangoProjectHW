from django.conf import settings
from django.core.mail import send_mail
from django.db import transaction
from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver

from .models import Task
from .models.task import Status


@receiver(
    pre_save,
    sender=Task,
    dispatch_uid="task_remember_previous_status",
)
def remember_previous_status(
    sender, instance, using, **kwargs
):
    instance._previous_status = None

    if kwargs.get("raw"):
        return

    update_fields = kwargs.get("update_fields")

    if update_fields is not None and "status" not in update_fields:
        return

    if instance._state.adding:
        return

    instance._previous_status = (
        sender._base_manager.using(using)
        .filter(pk=instance.pk)
        .values_list("status", flat=True)
        .first()
    )


@receiver(
    post_save,
    sender=Task,
    dispatch_uid="task_send_status_notification",
)
def task_status_changed(
    sender, instance, created, using, **kwargs
):
    if created or kwargs.get("raw"):
        return

    previous_status = getattr(
        instance, "_previous_status", None
    )

    if previous_status is None:
        return

    if previous_status == instance.status:
        return

    if not instance.owner_id or not instance.owner.email:
        return

    old_status = Status(previous_status).label
    new_status = instance.get_status_display()

    if instance.status == Status.DONE:
        subject = "Task Manager: Task completed"

        message = (
            f"Hello, {instance.owner.username}!\n\n"
            f'Your task "{instance.title}" '
            f"has been successfully completed!\n\n"
            f"Previous status: {old_status}\n"
            f"Current status: {new_status}\n\n"
            f"Congratulations!\n\n"
            f"Best regards,\n"
            f"Task Manager Team"
        )

    else:
        subject = "Task Manager: Task status updated"

        message = (
            f"Hello, {instance.owner.username}!\n\n"
            f'The status of your task "{instance.title}" '
            f"has been changed.\n\n"
            f"Previous status: {old_status}\n"
            f"Current status: {new_status}\n\n"
            f"Best regards,\n"
            f"Task Manager Team"
        )

    recipient_email = instance.owner.email

    transaction.on_commit(
        lambda: send_mail(
            subject=subject,
            message=message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[recipient_email],
        ),
        using=using,
    )