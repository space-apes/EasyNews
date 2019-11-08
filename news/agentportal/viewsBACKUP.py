from django.shortcuts import render
from django.http import HttpResponse
from .models import Agent, Customer, Delivery
# Create your views here.


#basic version
#def index(request):
#    return render(request, 'agentportal/index.html')

#def index(request):
	
#	agentName= "Agent1"
#	agentName=request.POST['agentName']
#	selectedAgent=Agent.objects.get(name=agentName)
#	nameAddressList=[]

#	for delivery in Delivery.objects.filter(agent=selectedAgent):
#		nameAddressList.append({'name':delivery.customer.name, 'address':delivery.customer.address})

#:set	return render(request, 'agentportal/index.html', {'nameAddressList':nameAddressList})

def index(request):
	agentName= "Agent1"
	selectedAgent=Agent.objects.get(name=agentName)
	nameAddressList=[]
	
	for delivery in Delivery.objects.filter(agent=selectedAgent):
		nameAddressList.append({'name':delivery.customer.name, 'address':delivery.customer.address})
	
	return render(request, 'agentportal/index.html', {'nameAddressList':nameAddressList})

