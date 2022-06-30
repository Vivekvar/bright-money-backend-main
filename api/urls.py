from django.urls import path, include
from .views import *


urlpatterns = [
    path('signup', register_client),
    path('createlinktoken', create_link_token),
    path('get_access_token', get_access_token),
    path('get_account', get_account),
    path('<slug>/', get_client),
    path('listen/<slug>', listen),
    path('transactions/get', get_transactions)
]
