from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator

# Create your models here.

class Character_Rating(models.Model):

    character = models.IntegerField()
    rating = models.FloatField(validators=[MaxValueValidator(10), MinValueValidator(1)])