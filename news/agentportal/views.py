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


#redirects to login page with no credentials	
def loginLanding(request):
	return render(request, 'agentportal/login.html')

#takes user credentials from login form
#if authenticated:
#	send user to show deliveries page with default settings
#else
#	send them back to login screen
def loginRedirect(request):
	username = request.POST['uName']
	password = request.POST['pWord']
	user = authenticate(request, username=username, password=password)
	if user is not None:
		login(request, user)
		return redirect('agentportal:agentportal-showDeliveriesDay')
	else:
	 	return redirect('/agentportal/')

#use django api to log out individual and send them back to login screen

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
		#if mode is not "day" it means we want deliveries from a range of dates. 
		#take form date for the beginning and end date.

		#first test whether form data was in valid yyyy-mm-dd format
		try:
			begDate = request.POST['startDateForm']
		except Exception as e:
			print("invalid start date submitted in form. setting to today's date.")
			begDate = todaysDate
		try:
			endDate = request.POST['endDateForm']
		except Exception as e:
			print("invalid end date submitted in form. setting to today's date.")
			endDate = todaysDate
		
	# if dates are out of order, swap them. 
	if endDate < begDate:
		tempDate = begDate
		begDate = endDate
		endDate = tempDate
	
	#for customer in Customer.objects.all():	
	#	if begDate.day < 20 and endDate.day > 20:
	#		dateNameAddressList.append({'date': date(todaysDate.year, todaysDate.month, 20), 'name': customer.name+"(BILL DUE FOR $)"+str(calcBillForMonth(customer, date.today(), 3.25))})
	
#	populate list nameAddressList with {date,name, address} dicts to fill the 	
	for delivery in Delivery.objects.filter(user=request.user).filter(date__gte=begDate).filter(date__lte=endDate):
		custName = delivery.customer.name
		dateNameAddressList.append({'date': delivery.date, 'name':custName, 'address':delivery.customer.address})
	
	
#	generate custom image url to generate google static map using address list	
	tailored_url = generateMapUrl([item['address'] for item in dateNameAddressList])
	
#	generate delivery message to show above list of deliveries. if there are more than 15 deliveries, 
#	append message explaining why markers do not show up on google maps image. 
	deliveryListMessage = ""
	if len(dateNameAddressList) >= 15:
		deliveryListMessage = "(google maps cannot display that many deliveries. limit to 15 or less) "
	deliveryListMessage +="from %s to %s" % (begDate, endDate)
	
	
	return render(request, 'agentportal/index.html', {'userName':request.user.username, 'dateNameAddressList':dateNameAddressList, 'mapURL':tailored_url, 'todaysDate': str(todaysDate), 'deliveryListMessage': deliveryListMessage })

#***DESCRIPTION***
#calculates total cost for all newspaper deliveries for a particular user in a particular month/year. 
#
#***SIGNATURE***
#(customer customerObject, dateInMonth string, singlePaperPrice float) -> float
#
#***PSEUDOCODE***
#calcBillForThisMonth(user, singlePaperPrice)
	#get the list of deliveries for this customer from the 1st to the 20th of the given date's month and year
	#get length of the list
	#return length * singlepaperPrice rounded to 2 decimal places
	
def calcBillForMonth(customer, dateInMonth, singlePaperPrice):
	deliveryList = Delivery.objects.filter(customer=customer).filter(date__gte=date(dateInMonth.year, dateInMonth.day, 1)).filter(date__lte=date(dateInMonth.year, dateInMonth.month, 20))
	return round(len(deliveryList)*singlePaperPrice, 2)
	

def generateMapUrl(addressList):		
	tailored_url = config.base_url+"&size=320x320&maptype=roadmap&markers=color:blue|"+"".join([address+"|" for address in addressList])+'&key='+config.api_key
	print(tailored_url)
	return tailored_url
