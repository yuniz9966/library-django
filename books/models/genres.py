from django.core.validators import MinLengthValidator
from django.db import models


class Genre(models.Model):
    name = models.CharField(
        max_length=25,
        unique=True,
        validators=[
            MinLengthValidator(4),
        ]
    )

    def __str__(self):
        return f"Genre: {self.name}"
