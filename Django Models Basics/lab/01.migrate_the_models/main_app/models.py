from django.db import models


class Employee(models.Model):
    name = models.CharField(max_length=30)
    email_address = models.EmailField()
    photo = models.URLField()
    birth_date = models.DateField()
    works_full_time = models.BooleanField()
    created_on = models.DateField(auto_now_add=True)


class Department(models.Model):
    class Locations(models.TextChoices):
        SOFIA = 'Sofia', 'Sofia'
        PLOVDIV = 'Plovdiv', 'Plovdiv'
        VARNA = 'Varna', 'Varna'
        BURGAS = 'Burgas', 'Burgas'

    # location_choices = [('Varna', 'Varna'), ('Plovdiv', 'Plovdiv'), ('Sofia', 'Sofia'), ('Burgas', 'Burgas')]
    code = models.CharField(max_length=10, primary_key=True, unique=True)
    name = models.CharField(max_length=50, unique=True)
    employees_count = models.PositiveIntegerField(default=1, verbose_name='Employees count')
    location = models.CharField(max_length=20, choices=Locations)
    last_edited_on = models.DateField(auto_now=True, editable=False)
