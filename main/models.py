from django.db import models

# Create your models here.
class CustomerRegister(models.Model):

    first_name=models.CharField(max_length=10)
    last_name=models.CharField(max_length=15)
    email=models.EmailField()
    mobile_no=models.IntegerField()
    dob=models.DateField()
    gender=models.CharField(max_length=7)

    def __str__(self):
        return self.first_name
    
class Age(models.Model):
    user_id=models.ForeignKey(CustomerRegister,on_delete=models.CASCADE)
    age=models.IntegerField()

 

class Hobbies(models.Model):
    user_id=models.ForeignKey(CustomerRegister,on_delete=models.CASCADE)
    hobby = models.CharField(max_length=50)


