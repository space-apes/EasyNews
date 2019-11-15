from django.shortcuts import render
from django.http import HttpResponse
from .models import Customer, Delivery
from django.contrib.auth.models import User
from datetime import date
# Create your views here.



#helper function to populate list of deliveries for today
#
#if the list of deliveries for today is empty
#	for all customers
#		if the current day does not fall within vacation dates for that customer
#			create a new delivery with current date, that customer, and set it to not-delivered

def populateDeliveries():
	todayDay = date.today().day
	if len(Delivery.objects.filter(date=date.today())) == 0:
		for curCustomer in Customer.objects.all():
			if not (todayDay >= curCustomer.vacationMonthDayBegin and todayDay <= curCustomer.vacationMonthDayEnd):
				td = Delivery(customer=curCustomer, user=curCustomer.user, date=date.today(), deliveredSuccessfully=False)
				td.save()

			





#initial loadup of agentportal will just pull up template with no
#dynamic content
#submission of form will pull uptemplate again using POST data
#to do db query to generate dynamic content.
def index(request):
	return render(request, 'agentportal/index.html')

def showDeliveries(request): 
	#get agentName from form
	agentName= request.POST['agentName']
	#if the form posted agent name is not in the list of names, just return a blank response
	if agentName not in [theuser.username for theuser in User.objects.all()]:
		return render(request, 'agentportal/index.html', {'agentName':'No such agent. Please re-enter name.'})
	#pull Agent entry from list of agents with matching name from form post	
	selectedAgent=User.objects.get(username=agentName)
	dateNameAddressList=[]
	#populate list nameAddressList with {date,name, address} dicts to fill the 	
	for delivery in Delivery.objects.filter(user=selectedAgent):
		dateNameAddressList.append({'date': delivery.date, 'name':delivery.customer.name, 'address':delivery.customer.address})
	
	return render(request, 'agentportal/index.html', {'agentName':agentName, 'dateNameAddressList':dateNameAddressList})

