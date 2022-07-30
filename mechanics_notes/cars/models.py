from django.db import models

# Create your models here.
from user_auth.models import User


class Car(models.Model):
    brand = models.CharField(max_length=250, default=None)
    model = models.CharField(max_length=250, default=None)
    year = models.IntegerField()
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=None)

    def as_json(self):
        return {
            "brand": self.brand,
            "model": self.model,
            "year": self.year,
            "id": self.id,
            "user_id": self.user.id
        }
