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
		return redirect('/agentportal/showDeliveries')
	else:
	 	return redirect('/agentportal/')

def logoutPage(request):
	logout(request)
	return redirect('/agentportal/')


#check if authenticated
#	if not, send to logout view
#
#
#
def showDeliveries(request): 
#	if not authenticated, return to login
	if not request.user.is_authenticated:
		return redirect('/agentportal/logout/')
#	grab current user's username
	print('request.user.username in showDeliveries in view %s' % request.user.username)
	#pull Agent entry from list of agents with matching name from form post	
	dateNameAddressList=[]
	#populate list nameAddressList with {date,name, address} dicts to fill the 	
	for delivery in Delivery.objects.filter(user=request.user):
		dateNameAddressList.append({'date': delivery.date, 'name':delivery.customer.name, 'address':delivery.customer.address})
	
#	return render(request, 'agentportal/index.html', {'agentName':agentName, 'dateNameAddressList':dateNameAddressList})
	return render(request, 'agentportal/index.html', {'userName':request.user.username, 'dateNameAddressList':dateNameAddressList, 'mapURL':generateMap(request)})
def generateMap(request):
	listOfAddresses = []
	for delivery in Delivery.objects.filter(user=request.user):
		listOfAddresses.append(delivery.customer.address)
	print(listOfAddresses[0])
	tailored_url = config.base_url+'center='+listOfAddresses[0]+'&size=320x320'+'&maptype=roadmap&markers=color:blue&key='+config.api_key
	print(tailored_url)
	return tailored_url
