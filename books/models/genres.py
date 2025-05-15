from django.core.validators import MinLengthValidator
from django.db import models

from books.models.user import User


class Genre(models.Model):
    name = models.CharField(
        max_length=25,
        unique=True,
        validators=[
            MinLengthValidator(4),
        ]
    )
    owner = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    def __str__(self):
        return f"Genre: {self.name}"

    class Meta:
        permissions = [
            ('can_get_statistic', 'Can get genres statistic'),
        ]
