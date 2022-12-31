from django.db import models
from django.contrib.auth.models import User

class Payment(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE,blank=True,null=True)
    name=models.CharField(max_length=20,blank=True,null=True)
    amount=models.CharField(max_length=20)
    order_id=models.CharField(max_length=200,blank=True)
    payment_id=models.CharField(max_length=200,blank=True)
    paid=models.BooleanField(default=False)
    
    def __str__(self):
        return str(self.user)