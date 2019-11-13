from django.contrib import admin
from agentportal.models import Customer, Agent
def set_agent1(modeladmin, request, queryset):
  queryset.update(agent=Agent.objects.get(pk=1))
  set_agent1.short_description="set these agents to agent 1"
  
class CustomerAdmin(admin.ModelAdmin):
  list_display = ['name','address']
  ordering = ['name']
  actions=[set_agent1]
  
admin.site.register(Customer, CustomerAdmin)
# Register your models here.
