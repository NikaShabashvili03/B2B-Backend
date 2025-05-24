from main.models.customer import Customer
from django.db import models

class Session(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    session_token = models.CharField(max_length=255, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()
    
    def is_valid(self):
         return f"{self.customer.email} - {self.session_token}"