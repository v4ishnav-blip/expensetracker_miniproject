from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Expenses(models.Model):
    title=models.CharField(max_length=100)

    CATEGORY_OPTIONS=[
        ('food','food'),
        ('rent','Rent'),
        ('Travel','Travel'),
        ('groceries','Groceries'),
        ('fuel','Fuel'),
        ('shopping','Shopping'),
        ('bills','Bills'),
        ('medical','Medical'),
        ('education','Education'),
        ('entertainment','Entertainment'),
        ('investment','Investment'),
        ('others','Others')
    ]
    
    category=models.CharField(max_length=100,choices=CATEGORY_OPTIONS)

    amount=models.FloatField()

    created_at=models.DateTimeField(auto_now_add=True)

    owner=models.ForeignKey(User,on_delete=models.CASCADE)

class Employee(models.Model):
    name=models.CharField(max_length=100)
    dept=models.CharField(max_length=299)
    location=models.CharField(max_length=122)
    salary=models.PositiveBigIntegerField()
    def __str__(self):
        return self.name