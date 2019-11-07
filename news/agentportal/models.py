from datetime import date
from django.db import models

# Create your models here.

class Agent(models.Model):
	name = models.CharField(max_length=120)

	def __str__(self):
		return self.name

class Customer(models.Model):
	name = models.CharField(max_length=120)
	address = models.CharField(max_length=120)
	agent = models.ForeignKey(Agent, on_delete=models.CASCADE)
	vacationMonthDayBegin = models.IntegerField(default=0)
	vacationMonthDayEnd = models.IntegerField(default=0)
	
	def __str__(self):
		return self.name
#should create one of each of these for every agent's customers per day at 00:00:01

#setting the default deliveredSuccessfully value to false
#setting the default date to the current date

#and importantly, allowing the agent to be able to change the value of deliveredSuccessfully through the site with checkboxes

class Delivery(models.Model):
	customer = models.ForeignKey(Customer, on_delete = models.CASCADE)
	agent = models.ForeignKey(Agent, on_delete = models.CASCADE)
	#field for tracking the delivery date of this particular delivery. 
	#setting auto_now=true makes it so the value is set to now upon creation of a Delivery instance
	#but it can not be modified later unless we change auto_now_add=True

	date = models.DateField(auto_now=True)
	deliveredSuccessfully = models.BooleanField(default=False)

