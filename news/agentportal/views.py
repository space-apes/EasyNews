from django.shortcuts import render,redirect
from django.http import HttpResponse
from .models import Customer, Delivery
from django.contrib.auth.models import User
from datetime import date
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from agentportal import config
from django import template
from django.http import HttpResponse
from django.utils import timezone
register = template.Library()
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

			
def loginLanding(request):
	return render(request, 'agentportal/login.html')


def loginRedirect(request):
	username = request.POST['uName']
	password = request.POST['pWord']
	user = authenticate(request, username=username, password=password)
	if user is not None:
		login(request, user)
		return redirect('agentportal:agentportal-showDeliveriesDay')
	else:
	 	return redirect('/agentportal/')

def logoutPage(request):
	logout(request)
	return redirect('/agentportal/')


##MAIN LOGIC FOR DELIVERY VIEWING
#	contains options for single day or range of dates (mode=day vs mode = range)
#	when transitioning from login screen, always set mode to day
#	when submitting form from this page, reloads the same page with mode=range, using values for beginning and end date from form 
#	
def showDeliveries(request, mode): 
#	if not authenticated, return to login
	if not request.user.is_authenticated:
		return redirect('/agentportal/logout/')
		
#	list of delivery info that will be passed to template to display deliveries
	dateNameAddressList=[]
	todaysDate = timezone.localtime(timezone.now()).date()
#	set mode to either deliver just today's deliveries or between a range. 		
	if mode=="day":
		begDate = todaysDate
		endDate = todaysDate
	else:
		begDate = request.POST['startDateForm']
		endDate = request.POST['endDateForm']
#		if someone submits empty date, set date to current date
		if not begDate:
			begdate = todaysDate
		if not endDate:
			endDate = todaysDate

#	populate list nameAddressList with {date,name, address} dicts to fill the 	
	for delivery in Delivery.objects.filter(user=request.user).filter(date__gte=begDate).filter(date__lte=endDate):
		dateNameAddressList.append({'date': delivery.date, 'name':delivery.customer.name, 'address':delivery.customer.address})
	
	tailored_url = config.base_url+'&size=320x320'+'&maptype=roadmap&markers=color:blue|'+"".join([dateNameAddress['address'] for dateNameAddress in dateNameAddressList])+'&key='+config.api_key
	print('tailored_url is: %s' % tailored_url)
	return render(request, 'agentportal/index.html', {'userName':request.user.username, 'dateNameAddressList':dateNameAddressList, 'mapURL':tailored_url, 'todaysDate': todaysDate})

def generateMap(request):
	listOfAddresses = []
	for delivery in Delivery.objects.filter(user=request.user):
		listOfAddresses.append(delivery.customer.address)
	print(listOfAddresses[0])
	tailored_url = config.base_url+'center='+listOfAddresses[0]+'&size=320x320'+'&maptype=roadmap&markers=color:blue&key='+config.api_key
	print(tailored_url)
	return tailored_url
