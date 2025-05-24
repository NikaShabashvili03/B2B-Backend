from django.db import models
from django.contrib.auth.models import AbstractBaseUser

class Customer(AbstractBaseUser):
    firstname = models.CharField(max_length=255)
    lastname = models.CharField(max_length=255)
    email = models.EmailField(unique=True)

    last_login = models.DateTimeField(null=True, blank=True)
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['firstname', 'lastname']

    def save(self, *args, **kwargs):
        self.firstname = self.firstname.capitalize()
        self.lastname = self.lastname.capitalize()
        if self.pk is None: 
            self.set_password(self.password) 
        super().save(*args, **kwargs)


    company_name = models.CharField(max_length=255)
    tax_id = models.CharField(max_length=50, unique=True, help_text="Business tax identification number")
    contact_number = models.CharField(max_length=20, blank=True)
    address = models.TextField(blank=True)
    account_status = models.CharField(
        max_length=20, 
        choices=[('Active', 'Active'), ('Suspended', 'Suspended'), ('Pending', 'Pending')], 
        default='Active'
    )

    def __str__(self):
        return f"{self.company_name} | {self.firstname} - {self.lastname}"