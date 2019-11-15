from django.contrib import admin
from agentportal.models import Customer, Delivery
# Register your models here.

#EXAMPLE FOR HOW TO MAKE AN ADMIN ACTION IN ADMIN PORTAL 
#FOR ALL CUSTOMERS
#def set_agent1(modeladmin, request, queryset):
#	queryset.update(agent=Agent.objects.get(pk=1))
#	set_agent1.short_description="set these agents to agent1"

class CustomerAdmin(admin.ModelAdmin):
	list_display = ['name', 'address', 'user', 'vacationMonthDayBegin', 'vacationMonthDayEnd']
	ordering = ['name']
#YOU WOULD NEED THIS TOO	
#	actions=[set_agent1]

class DeliveryAdmin(admin.ModelAdmin):
	list_display = ['date', 'user', 'customer', 'deliveredSuccessfully']
	ordering = ['date']

admin.site.register(Customer, CustomerAdmin)
admin.site.register(Delivery, DeliveryAdmin)
