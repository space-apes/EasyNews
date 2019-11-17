from django.shortcuts import render,redirect
from django.http import HttpResponse
from .models import Customer, Delivery
from django.contrib.auth.models import User
from datetime import date
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
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


#check if authenticated
#	if not, send to logout view
#
#
#
def showDeliveries(request, mode): 
#	if not authenticated, return to login
	if not request.user.is_authenticated:
		return redirect('/agentportal/logout/')
		
#	list of delivery info that will be passed to template to display deliveries
	dateNameAddressList=[]

#	set mode to either deliver just today's deliveries or between a range. 		
	if mode=="day":
		begDate = date.today()
		endDate = date.today()
	else:
		begDate = request.POST['startDateForm']
		endDate = request.POST['endDateForm']
		print("you chose to see deliveries in range mode! post date for begDate is %s and endDate is %s" % (begDate, endDate))
		print("whereas the format for date.today is %s" % (date.today()))
	
#	populate list nameAddressList with {date,name, address} dicts to fill the 	
	for delivery in Delivery.objects.filter(user=request.user).filter(date__gte=begDate).filter(date__lte=endDate):
		dateNameAddressList.append({'date': delivery.date, 'name':delivery.customer.name, 'address':delivery.customer.address})
	
#	return render(request, 'agentportal/index.html', {'agentName':agentName, 'dateNameAddressList':dateNameAddressList})
	return render(request, 'agentportal/index.html', {'userName':request.user.username, 'dateNameAddressList':dateNameAddressList})
