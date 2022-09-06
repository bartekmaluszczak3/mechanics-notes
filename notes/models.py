from django.db import models
from cars.models import Car

class Note(models.Model):
    description = models.CharField(max_length=250, default=None)
    date = models.DateField()
    mileage = models.IntegerField()
    repair = models.CharField(max_length=250, default=None)
    next_repair = models.CharField(max_length=250, default=None, null=True)
    car = models.ForeignKey(Car, on_delete=models.CASCADE)

    def as_json(self):
        return {
            "description": self.description,
            "date": self.date,
            "mileage": self.mileage,
            "repair": self.repair,
            "next_repair": self.next_repair,
            'car_id': self.car.id,
            "id": self.id
        }