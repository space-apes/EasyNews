from agentportal.models import Customer, Delivery
from django.contrib.auth.models import User
from datetime import date
from django.core.management.base import BaseCommand,CommandError
# Create your views here.



#helper function to populate list of deliveries for today
#
#if the list of deliveries for today is empty
#	for all customers
#		if the current day does not fall within vacation dates for that customer
#			create a new delivery with current date, that customer, and set it to not-delivered

def populateDeliveries():
	todayDay = date.today().day
	deliveryCount = 0
	if len(Delivery.objects.filter(date=date.today())) == 0:
		for curCustomer in Customer.objects.all():
			if not (todayDay >= curCustomer.vacationMonthDayBegin and todayDay <= curCustomer.vacationMonthDayEnd):
				td = Delivery(customer=curCustomer, user=curCustomer.user, date=date.today(), deliveredSuccessfully=False)
				td.save()
				deliveryCount+=1
	return deliveryCount


class Command(BaseCommand):
	help='populates list of deliveries if there are none for today'
	def handle(self, *args, **options):
		dAdded = populateDeliveries()
		
		self.stdout.write("%s: executed news/management/populate.py to populate delivery list for today. added %d more deliveries to database." % (date.today(), dAdded))

