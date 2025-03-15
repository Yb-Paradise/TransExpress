from django.db import models

# Create your models here.
class Quote(models.Model):
    departure = models.CharField(max_length=255)
    delivery = models.CharField(max_length=20)
    weight = models.CharField(max_length=255)
    dimension = models.IntegerField(max_length=25)
    name = models.CharField(max_length=50)
    email = models.EmailField()
    phone = models.IntegerField(max_length=20)
    message = models.TextField()


    def __str__(self):
        return f"{self.name} - {self.delivery} ({self.phone})"



class Transaction(models.Model):
    phone_number = models.CharField(max_length=15)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    transaction_id = models.CharField(max_length=100, unique=True)
    status = models.CharField(max_length=20, choices=[('Success', 'Success'), ('Failed', 'Failed')])
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.phone_number} - {self.amount} - {self.status}"
