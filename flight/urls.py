"""
URL configuration for train project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.views.generic import TemplateView
from myapp import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',TemplateView.as_view(template_name='index.html')),
    path('login/', views.login, name='login'),
    path('register/', views.register, name='register'),
    path('getProfile/', views.get_profile, name='get_profile'),
    path('changePass/', views.change_password, name='change_password'),
    path('changeProfile/', views.change_profile, name='change_profile'),
    path('getRelation/',views.get_relation,name='get_relation'),
    path('addRelation/',views.add_relation,name='add_relation'),
    path('delRelation/',views.del_relation,name='del_relation'),
    path('getpTicket/', views.getp_ticket, name='getp_ticket'),
    path('getPassenger/', views.get_passenger, name='get_passenger'),
    path('book/', views.book_ticket, name='book_ticket'),
    path('bookedTickets/', views.booked_tickets, name='booked_tickets'),
    path('purchase/', views.purchase_ticket, name='purchase_ticket'),
    path('cancelTicket/', views.cancel_ticket, name='cancel_ticket'),
    path('orderedTickets/', views.order_tickets, name='order_tickets'),
    path('getArrange/', views.mget_ticket, name='mget_tickets'),
    path('changeArrange/', views.change_arrange, name='change_arrange'),
    path('delArrange/', views.del_arrange, name='del_arrange'),
    path('getTrain/', views.get_train, name='get_train'),
    path('mgetTrain/', views.mget_train, name='mget_train'),
    path('saveArrange/', views.save_arrange, name='save_arrange'),
    path('changeTrain/', views.change_train, name='change_train'),
    path('delTrain/', views.del_train, name='del_arrange'),
    path('saveTrain/', views.save_train, name='save_train'),
    path('getTicket/', views.get_ticket, name='get_ticket'),
    path('getTicketMore/', views.get_ticket_more, name='get_ticket_more'),
    path('delTicket/', views.del_ticket, name='del_ticket'),
    path('delTicketBatch/', views.del_ticket_batch, name='del_ticket_batch'),
    path('mgetPassenger/', views.mget_passenger, name='mget_passenger'),
    path('delPassenger/', views.del_passenger, name='del_passenger'),
    path('delPassengerBatch/', views.del_passenger_batch, name='del_passenger_batch'),
    path('getAccount/', views.get_account, name='get_account'),
    path('resetAccount/', views.reset_account, name='reset_account'),
    path('delAccount/', views.del_account, name='del_account'),
    path('delAccountBatch/', views.del_account_batch, name='del_account_batch'),
    path('getSchedule/', views.getSchedule,name="getmSchedule"),
    path('addStop/', views.add_stop, name='add_stop'),
    path('getStops/', views.get_stops, name='get_stops'),
    path('delStop/', views.del_stop, name='del_stop'),
]
