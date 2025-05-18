from django.db.models.signals import post_save
from django.dispatch import receiver

from books.models import Genre


@receiver(post_save, sender=Genre)
def genre_created_signal(sender, instance, created, **kwargs):
    if created:
        print("=" * 100)
        print("=" * 100)
        print()
        print(f"New Genre was created. It's {instance.name}")
        print()
        print("=" * 100)
        print("=" * 100)
    else:
        print("=" * 100)
        print("=" * 100)
        print()
        print(f"The genre was updated. Now it's {instance.name}")
        print()
        print("=" * 100)
        print("=" * 100)
