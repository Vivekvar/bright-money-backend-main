from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from rest_framework.response import Response
from rest_framework import serializers, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import ClientSerializer, ItemSerializer
from rest_framework.parsers import JSONParser
from .models import client, item
from plaid.api import accounts
import plaid
from plaid import Client
import json
import datetime

# Object ( Plaid client )
pclient = plaid.Client(
    client_id='62bd78d63c450d00141a6789',
    secret='12960714a02ed24cd97b6170066552',
    environment='sandbox',
    api_version='2019-05-29',
	public_key=''
)

# Test Route
@api_view(['GET', ])
@permission_classes((IsAuthenticated,))
def get_client(request, slug):
    try:
        current_user = client.objects.get(username=slug)
    except client.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    data = ClientSerializer(current_user)
    return Response(data.data)


# Registeing the User,


@api_view(['POST', ])
def register_client(request):
    data = JSONParser().parse(request)
    current_client = {}
    try:
        current_client = client.objects.get(username=data['username'])
    except client.DoesNotExist:
        serialized_data = ClientSerializer(data=data)
        user = client(
            name=data['name'], username=data['username'], password=data['password'])
        password = data["password"]
        user.set_password(password)
        if(serialized_data.is_valid()):
            user.save()
        current_client = client.objects.get(username=data['username'])
        refresh = RefreshToken.for_user(current_client)
        print(refresh.access_token)
        data["password"] = ""
        return Response(data)
    data["error"] = "User Already Exists"
    data['password'] = ""
    return Response(data)


# Genrating Link_token and creating web hook url when the user is loggedin
@api_view(['POST', ])
@permission_classes((IsAuthenticated,))
def create_link_token(request):
    data = {
        'user': {
            'client_user_id': f"{request.user.id}"
        },
        'products': ["transactions"],
        'client_name': f"{request.user.name}",
        'country_codes': ['US'],
        'language': 'en',
        'webhook': f"https://bright-money-backend-plaid.herokuapp.com/api/listen/{request.user.id}"
    }
    response = {'link_token': pclient.post('link/token/create', data)}
    link_token = response['link_token']
    return JsonResponse(link_token)


# Web Hook url return all accounts details associated with given user
# At present this just sends the transactions as JSON, but we can send these updates to email, using celery
@api_view(['POST', 'GET', ])
def listen(request, slug):
    result = ''
    data = {}
    try:
        result = item.objects.filter(customer=slug)
    except item.DoesNotExist:
        data['Error'] = "No Such User Found"
        return Response(data)
    accounts_response = []
    for elem in result:
        accounts_response.append(pclient.Accounts.get(elem.access_token))
    print(accounts_response)
    return Response(accounts_response)


# API for fetching Access Token and Saving the Access Token and Item in Database
@api_view(['POST', ])
@permission_classes((IsAuthenticated,))
def get_access_token(request):
    data = json.loads(request.body)
    result = {}
    exchange_response = \
        pclient.Item.public_token.exchange(data['public_token'])
    item_id = exchange_response['item_id']
    result['access_token'] = exchange_response['access_token']
    result['item_id'] = f"{item_id}"
    result['customer'] = f"{request.user.id}"
    message = {}
    serialized_data = ItemSerializer(data=result)
    if(serialized_data.is_valid()):
        serialized_data.save()
        message['message'] = "Data Saved"
        return Response(message)
    message['error'] = "Something went Wrong"
    return Response(message)


# API for getting info of all the accounts associated with the user
@api_view(['GET', ])
@permission_classes((IsAuthenticated,))
def get_account(request):
    result = ''
    try:
        result = item.objects.filter(customer=request.user.id)
    except item.DoesNotExist:
        data = {}
        data['err'] = "User Not Registered with any bank"
        return Response(data)
    accounts_response = []
    for elem in result:
        accounts_response.append(pclient.Accounts.get(elem.access_token))
    # trying to hit the web hook
    # Asynchronous Task For testing web hook only
    resp = pclient.Sandbox.item.fire_webhook(
        elem.access_token, 'DEFAULT_UPDATE')
    return Response(accounts_response)


# For getting all the transactions of the user of all the accounts linked pf last two years
@api_view(['GET', ])
@permission_classes((IsAuthenticated,))
def get_transactions(request):
    result = ''
    try:
        result = item.objects.filter(customer=request.user.id)
    except item.DoesNotExist:
        data = {}
        data['err'] = "User Not Registered with any bank"
        return Response(data)
    account_data = []
    for elem in result:
        response = pclient.Transactions.get(
            elem.access_token, start_date='2019-08-08', end_date=f"{datetime.date.today()}")
        account_data.append(response['transactions'])
    return Response(account_data)
