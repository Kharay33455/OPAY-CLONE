from django.urls import path
from . import views

app_name = 'base'

urlpatterns = [
    path('', views.logged_out, name = 'logged_out'),
    path('<slug:slug>/', views.home, name='home'),
    path('<slug:slug>/transfer/', views.transfer, name='transfer'),
    path('<slug:slug>/transfer/toopayaccount', views.to_opay_account, name = 'to_opay_account'),
    path('<slug:slug>/recents.html/', views.recent_transactions, name = 'recents' ),
    path('<slug:slug>/favorites.html', views.favorites_transactions, name= 'favorites'),
    path('<slug:slug>/transfer/toopayaccount/transfer_operator/<int:account_number>/', views.transfer_amount, name = 'tfamount'),
    path('<slug:slug>/transfer/toopayaccount/transfer_operator', views.transfer_operator, name = "tfoperator"),
    path('<slug:slug>/transfer/toopayaccount/tranfer_operator/<int:account_number>/amount/', views.amount_operator, name = 'amount_op' ),
    path('<slug:slug>/transfer/toopayaccount/tranfer_operator/<int:account_number>/amount/<int:amount>', views.transaction_operator, name = "toperator"),
    path('<slug:slug>/transaction_history/', views.transaction_history, name = 'tfhistory'),
    path('<slug:slug>/transaction_history/<int:transaction_id>/', views.transaction_details, name = 'tfdetails'),

]