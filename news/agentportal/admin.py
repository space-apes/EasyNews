from django.contrib import admin
from agentportal.models import Customer, Agent
def CustomerAdmin(admin.ModelAdmin):
  list_display = ['name','address']
  ordering = ['name']
  
 admin.site.register(Article, ArticleAdmin)
# Register your models here.
