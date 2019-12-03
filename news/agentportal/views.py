#***EASYNEWS NEWSPAPER DELIVERY SYSTEM VIEWS****
#
#Andrew Aguilar
#Brian Smith
#Courtney Castrey
#Hilario Balajadia Jr. 
#Matthew Siewierski
#Shinaola Agbede
#
#CSC-581 Software Engineering
#Fall 2019
#California State University Dominguez Hills

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
from datetime import date
register = template.Library()

#****************VIEWS**********************: 
#these functions perform all server side computation and ultimately direct user's browser to new page.
#After a user goes to a particular url, they will call one of these view functions. The mapping of URL->view function is contained in
#agentportal.urls.py and /urls.py files.
#The view functions can: 	
#
#	-take POSTed user input from web forms, 
#	-perform CRUD database operations (such as reading data), 
#	-perform server-side computation
#	-direct the browser to load certain template HTML/CSS files, inserting dynamic content
#
#View functions may have other optional parameters, but always take in a request object parameter containing all 
#information about the web request, and always produce an HttpResponse object with either redirect() or render()
#	
#CONTENTS:
#1. helper functions
#2. simple views (that mostly just redirect browser to load either a diff view function or to load a template html/css file)
#3. showDeliveries: contains most of logic for agentportal











#***HELPERFUNCTION***: calcBillForThisMonth
#DESCRIPTION
#calculates total cost for all newspaper deliveries for a particular user in a particular month/year. 
#SIGNATURE
#(customer customerObject, billDate string, singlePaperPrice float) -> float
#PSEUDOCODE
#calcBillForThisMonth(user, singlePaperPrice)
	#get the list of deliveries for this customer from the 1st to the 20th of the given date's month and year
	#get length of the list
	#return length * singlepaperPrice rounded to 2 decimal places
	
def calcBillForMonth(customer, billDate, singlePaperPrice):
	deliveryList = Delivery.objects.filter(customer=customer).filter(date__gte=date(billDate.year, billDate.month-1, 21)).filter(date__lte=date(billDate.year, billDate.month, 20))
	return round(len(deliveryList)*singlePaperPrice, 2)
	
#***HELPERFUNCTION***: generateMapUrl
#DESCRIPTION
#creates url containing list of addresses to deliver to formatted to be used by Google Static Images API to generate an image.
#SIGNATURE
#(stringList addressList)->string
def generateMapUrl(addressList):		
	tailored_url = config.base_url+"&size=320x320&maptype=roadmap&markers=color:blue|"+"".join([address+"|" for address in addressList])+'&key='+config.api_key
	print(tailored_url)
	return tailored_url

#***VIEW FUNCTION***: loginLanding
#DESCRIPTION
#redirects to login page with no authentication cr	
#SIGNATURE
#(httpRequest)->HttpResponse
def loginLanding(request):
	return render(request, 'agentportal/login.html')

#***VIEW FUNCTION***: loginRedirect
#DESCRIPTION
#takes user credentials from login form and either redirects them to showDeliveriesDay view or back to the login page
#SIGNATURE
#(httpRequest)->HttpResponse
#PSEUDOCODE
#
#retrieve username and a password from form fields after being submitted
#use django's built-in user authentication to create a user object 
#if user was discovered with given username and password
#	set status to logged in
#	redirect to showDeliveries-Day view
#else
#	redirect to login view without setting status to logged in

def loginRedirect(request):
	username = request.POST['uName']
	password = request.POST['pWord']
	user = authenticate(request, username=username, password=password)
	if user is not None:
		login(request, user)
		return redirect('agentportal:agentportal-showDeliveriesDay')
	else:
	 	return redirect('/agentportal/')

#***VIEW FUNCTION***: logoutPage
#DESCRIPTION
#use django api to log out individual and send them back to login screen
#SIGNATURE
#(httpReques)->HttpResponse

def logoutPage(request):
	logout(request)
	return redirect('/agentportal/')


#***VIEW FUNCTION***: showDeliveries
#DESCRIPTION
#This is the main view utilized by our users. The purpose is to generate a page relevant to the logged-in delivery agent 
#for them to learn information about their current and or past deliveries including when,where, to whom, and whether bills 
#are due in a given range of dates by providing a list and a map image of each delivery location.
#ShowDeliveries has 2 modes of operation: 
#	-(default when transitioning from login page): display delivery information for given user for current day
#	-take in form data about range of dages and display delivery information for those dates 				
#
#SIGNATURE
#(httpRequest, string mode)->HttpResponse	
#
#CONSTRAINTS
#	-only display delivery information relevant to logged in user(newspaper agent)
#	-do not generate deliveries for customers that are on vacation
#	-if range of deliveries includes the 20th of that month, generate a special delivery that includes each customer's
#		bill using calcBillForMonth helper function..
#	-display up to 15 of the delivery addresses on a visual map
#
#PSEUDOCODE
#if the user is not authenticated
#	redirect them to logout page	
#if mode is set to day
#	set begDate and endDate variables to the current day
#else
#	set begDate and endDate by using POSTed form data
#if form data is not valid
#	give a warning and set endDate and begDate to current day
#convert begDate and endDate variables to datetime.date() objects
#if the endDate is before begDate
#	swap the values
# for all deliveries with given user that are >= begDate and are <=endDate
#	append a dict to the dateNameAddressList 
#if the 20th falls between endDate and begDate
#	for all customers
#		append a entry to dateNameAddressList including bill calculated with calcBillForMonth helper function
#if number of items in dateNameAddressList is greater than 15
#	generate a warning message that Google maps API can only handle 15 markers
#generate the url for google static maps api by passing information from dateNameAddressList
#return HttpResponse object using same html file as template, but passing on:
#	-username
#	-dateNameAddressList
#	-google maps url
#	-delivery message
#	-current date

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
	
	#the form submission changes the datatype of these variables from datetime.date() objects to 
	#strings. for code consistency, let's check if they are date() objects, and if not, make them date objects
	if not isinstance(begDate, date):
		begDateList = list(map(lambda x: int(x), begDate.split('-')))
		begDate = date(begDateList[0], begDateList[1], begDateList[2])
	if not isinstance(endDate, date):
		endDateList = list(map(lambda x: int(x), endDate.split('-')))
		endDate = date(endDateList[0], endDateList[1],endDateList[2])
	
	# if dates are out of order, swap them. 
	if endDate < begDate:
		tempDate = begDate
		begDate = endDate
		endDate = tempDate	
		
#	populate list nameAddressList with {date,name, address} dicts to fill the view 	
	for delivery in Delivery.objects.filter(user=request.user).filter(date__gte=begDate).filter(date__lte=endDate):
		custName = delivery.customer.name
		dateNameAddressList.append({'date': delivery.date, 'name':custName, 'address':delivery.customer.address})	
		
#	add a an entry for the bill if the 20th falls between begDate and endDate for all years and months that are spanned from begDate and endDate
	for yearNum in range(begDate.year, endDate.year+1):
		for monthNum in range(begDate.month, endDate.month+1):	
			billDate = date(yearNum, monthNum, 20)	
			if begDate <= billDate and endDate >= billDate:
				for customer in Customer.objects.filter(user=request.user):
					dateNameAddressList.append({'date': str(date(yearNum,monthNum-1, 21))+" TO "+str(billDate), 'name': "(BILL DUE for "+str(calcBillForMonth(customer, billDate, .87))+"):"+customer.name, 'address':customer.address})	
	

#	generate delivery message to show above list of deliveries. if there are more than 15 deliveries, 
#	append message explaining why markers do not show up on google maps image. 
	deliveryListMessage = ""
	if len(dateNameAddressList) >= 15:
		deliveryListMessage = "(google maps cannot display that many deliveries. limit to 15 or less) "
	deliveryListMessage +="from %s to %s" % (begDate, endDate)
	
#	generate custom image url to generate google static map using address list	
	tailored_url = generateMapUrl([item['address'] for item in dateNameAddressList])
	
	return render(request, 'agentportal/index.html', {'userName':request.user.username, 'dateNameAddressList':dateNameAddressList, 'mapURL':tailored_url, 'todaysDate': str(todaysDate), 'endDate': str(endDate), 'begDate': str(begDate), 'deliveryListMessage': deliveryListMessage })

