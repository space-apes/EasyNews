from django.urls import path
from . import views

app_name = 'agentportal'

urlpatterns = [
        path('', views.loginLanding, name='agentportal-loginLanding'),
	path('loginRedirect', views.loginRedirect, name='agentportal-loginRedirect'),
	path('showDeliveries', views.showDeliveries, name='agentportal-showDeliveries'),
	path('logout', views.logoutPage, name='agentportal-logout')
]

