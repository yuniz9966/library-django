from django.core.mail import send_mail
from django.db.models.signals import post_save
from django.dispatch import receiver

from books.models import User


@receiver(post_save, sender=User)
def notify_admin_with_moderator_create(sender, instance, created, **kwargs):
    if created and instance.is_staff and instance.role == "MODERATOR":
        send_mail(
            subject='New Moderator',
            message=f'Moderator {instance.username} was added to the system.',
            from_email='no-reply.160924_ptm@gmail.com',
            recipient_list=['admin.mail@gmail.com'],
            fail_silently=False
        )
