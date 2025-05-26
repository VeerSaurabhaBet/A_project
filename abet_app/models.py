from django.db import models

class Employee(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    department = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Asset(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='assets')
    asset_name = models.CharField(max_length=100)
    asset_type = models.CharField(max_length=50)
    serial_number = models.CharField(max_length=100)
    # assigned_date = models.DateField()
    assigned_date = models.DateField(null=True, blank=True)

    def __str__(self):
        return f"{self.asset_name} ({self.serial_number})"
