from django.urls import path
from . import views

app_name = 'agentportal'

urlpatterns = [
        path('', views.loginLanding, name='agentportal-loginLanding'),
	path('loginRedirect', views.loginRedirect, name='agentportal-loginRedirect'),
	path('showDeliveriesDay', views.showDeliveries, {'mode' : 'day'}, name='agentportal-showDeliveriesDay'),
	path('showDeliveriesRange', views.showDeliveries, {'mode' : 'range'}, name='agentportal-showDeliveriesRange'),
	path('logout', views.logoutPage, name='agentportal-logout'),
	path('updateDeliveryStatus', views.updateDeliveryStatus, name='agentportal-updateDeliveryStatus')
]

