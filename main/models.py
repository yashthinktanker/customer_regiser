from django.db import models

# Create your models here.
class CustomerRegister(models.Model):

    first_name=models.CharField(max_length=10)
    last_name=models.CharField(max_length=15)
    email=models.EmailField()
    password=models.TextField()
    mobile_no=models.BigIntegerField()
    dob=models.DateField()
    gender=models.CharField(max_length=7)

    def __str__(self):
        return self.first_name
    
class Age(models.Model):
    user_id=models.OneToOneField(CustomerRegister,on_delete=models.CASCADE,related_name='age')
    age=models.IntegerField()

 

class Hobbies(models.Model):
    user_id=models.ForeignKey(CustomerRegister,on_delete=models.CASCADE,related_name='hobby')
    hobby = models.CharField(max_length=50)


