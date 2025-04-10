from django.db import models

# Create your models here.
from django.db import models

class Income(models.Model):
    date = models.DateField()
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    source = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.date} - {self.amount} - {self.source}"

class Expense(models.Model):
    date = models.DateField()
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.CharField(max_length=255)
    description = models.TextField()

    def __str__(self):
        return f"{self.date} - {self.amount} - {self.category}"