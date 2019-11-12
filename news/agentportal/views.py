from django.shortcuts import render
from django.http import HttpResponse
from .models import Agent, Customer, Delivery
# Create your views here.


#basic version
#def index(request):
#    return render(request, 'agentportal/index.html')




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
	if agentName not in list(map(lambda x: x.name, Agent.objects.all())):
		return render(request, 'agentportal/index.html', {'agentName':'No such agent. Please re-enter name.'})

	#pull Agent entry from list of agents with matching name from form post	
	selectedAgent=Agent.objects.get(name=agentName)
	dateNameAddressList=[]
	#populate list nameAddressList with {date,name, address} dicts to fill the 	
	for delivery in Delivery.objects.filter(agent=selectedAgent):
		dateNameAddressList.append({'date': delivery.date, 'name':delivery.customer.name, 'address':delivery.customer.address})
	
	return render(request, 'agentportal/index.html', {'agentName':agentName, 'dateNameAddressList':dateNameAddressList})

