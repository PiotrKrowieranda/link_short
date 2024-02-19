from django.db import models
from django.contrib.auth.models import User
from django.core.validators import URLValidator


class ShortenedLink(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    original_url = models.URLField(validators=[URLValidator()])
    shortened_url = models.CharField(max_length=100, unique=True)



