from django.conf import settings
from django.db import models
from django.utils import timezone
from django.core.validators import MaxValueValidator, MinValueValidator

# Create your models here.
class User(models.Model):
    user_id = models.CharField(max_length=34, unique=True)
    x_open = models.SmallIntegerField(default=0, validators=[MinValueValidator(0)])
    y_open = models.SmallIntegerField(default=0, validators=[MinValueValidator(0)])
    z_open = models.SmallIntegerField(default=0, validators=[MinValueValidator(0)])
    x_close = models.SmallIntegerField(default=0, validators=[MinValueValidator(0)])
    y_close = models.SmallIntegerField(default=0, validators=[MinValueValidator(0)])
    z_close = models.SmallIntegerField(default=0, validators=[MinValueValidator(0)])
    created_date = models.DateTimeField(default=timezone.now())
