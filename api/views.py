
from operator import le
from pydoc import resolve
from unicodedata import name
from urllib import request
from wsgiref import headers
from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from http import HTTPStatus
from .models import Account, Userm, Opportunity
import requests

# Root Endpoint
def home(request):
    content = ''
    try:
        response = JsonResponse({'status':'true','message':"Hello Usesr, Welcome to Clientell. Use our endpoints to import and view the data. Reac the documentation for getting started."}, status=HTTPStatus.OK)
    
    except Exception as e:
        response = JsonResponse({'status':'false','message':"Inernal Server Error. We are sorry for inconvenience."}, status=HTTPStatus.INTERNAL_SERVER_ERROR)

    return response

def getAccessToken():
    consumerKey =  '3MVG9pRzvMkjMb6mzmTGES2xCuzah2ZLsa4mrMhvWAwqvYMA63A.xg5sU7nKw8sLm7CO3y5tA1UrTShBnrJTd'
    consumersecret = '153D2FF33316A59B85083F3F2754CB4C6D5C34CB5957CCCC3F25D6553DFEF6F1'
    username = 'ruthuparna1998@gmail.com'
    password = 'clientell123'

    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
    }

    data = f'grant_type=password&client_id={consumerKey}&client_secret={consumersecret}&username={username}&password={password}'
    # Fetcing the salesforces Data
    response = requests.post(f'https://clientell3-dev-ed.my.salesforce.com/services/oauth2/token', headers=headers, data=data)
    responseData = response.json()
    return responseData["access_token"]

def getData(accessToken,params):
    headers = {
        'Authorization': f'Bearer {accessToken}',
        'X-PrettyPrint': '1',
    }
 
    # Request For Accounts Ids and Names and store in database
    response = requests.get('https://clientell3-dev-ed.my.salesforce.com/services/data/v55.0/query', params=params, headers=headers)

    data = response.json()
    return data


# Function to clear the database
def clearDatabase():
    Userm.objects.all().delete()
    Account.objects.all().delete()
    Opportunity.objects.all().delete()

# Store users in Database
def createUser(data):
    usrModelList = []
    for i in data:
        usrModelList.append ( Userm(name=i['name'],id=i['id']) )
    Userm.objects.bulk_create(usrModelList)


# Store Account in Database
def createAccount(data):
    accountModelList = []
    for i in data:
        accountModelList.append ( Account(name=i['name'],id=i['id']) )
    Account.objects.bulk_create(accountModelList)

# Store Opportunity in Database
def createOpprotunity(data):
    opportunityModelList = []
    for i in data:
        opportunityModelList.append( Opportunity(id=i['id'],name=i['name'],amount=i['amount'], accountId=i['accountId'],userId=i['ownerId']) )
   
      
    
    Opportunity.objects.bulk_create(opportunityModelList)
    
        
    
  
   


    

# An import API to import data from salesforce
def importData(response):
    try:
        # Api call to get the Access Token
        accessToken = getAccessToken()

        # Getting Account Data ( Id Name )
        params = {
        'q': 'SELECT name from Account',
        }
        data = getData(accessToken,params)
        accountValues = []
        for i in data['records']:
            temp = {"id":i['attributes']['url'][-18:-1],"name":i['Name']}
            accountValues.append(temp)


        # Request For Users Ids and Names and store in database
        params = {
        'q': 'SELECT name from User',
        }
        data = getData(accessToken,params)
        userValues = []
        for i in data['records']:
            temp = {"id":i['attributes']['url'][-18:-1],"name":i['Name']}
            userValues.append(temp)

        # Request For Opportunity Table Data ( id,name,amount,accountId,ownerId )
        params = {
        'q': 'SELECT id from Opportunity',
        }
        data = getData(accessToken,params)
        opportunitiesId = [i["Id"] for i in data['records']]
        idurl = ','.join(opportunitiesId)

        # Fetching multiple data fields with the help of all the opportunity ids
        url = f'https://clientell3-dev-ed.my.salesforce.com/services/data/v55.0/composite/sobjects/Opportunity?ids={idurl}&fields=id,name,amount,accountId,ownerId'
        headers = {
            'Authorization': f'Bearer {accessToken}',
            'X-PrettyPrint': '1',
        }
        response = requests.get(url, headers=headers)
        responseData = response.json()
        opportunitiesValues = []
        for i in responseData:
            temp = {"id":i['Id'],"name":i['Name'],"amount":i["Amount"],"accountId":i['AccountId'],'ownerId':i['OwnerId']}
            opportunitiesValues.append(temp)

        # Storing the user, opportunity, accoutns in database after clearing it
        clearDatabase() 
        createUser(userValues)
        createAccount(accountValues)
        createOpprotunity(opportunitiesValues)

        return JsonResponse({'status':'true','writtenObjects':
        {"User":len(userValues),"Accounts":len(accountValues), "Opportunities":len(opportunitiesValues)}, "totalWrittenObjects":len(userValues)+len(accountValues)+len(opportunitiesValues) },status=HTTPStatus.OK)

    except Exception as e:
        print(e)
        return JsonResponse({'status':'false','message':"Inernal Server Error. We are sorry for inconvenience."}, status=HTTPStatus.INTERNAL_SERVER_ERROR)

    
    


# An API to view all Opportunties
def opportunities(response):
    try:
        pass
    except Exception as e:
        return JsonResponse({'status':'false','message':"Inernal Server Error. We are sorry for inconvenience."}, status=HTTPStatus.INTERNAL_SERVER_ERROR)

    return HttpResponse("opportunities Data")

# An API to view all Accounts
def accounts(response):
    try:
        pass
    except Exception as e:
        return JsonResponse({'status':'false','message':"Inernal Server Error. We are sorry for inconvenience."}, status=HTTPStatus.INTERNAL_SERVER_ERROR)

# An API to view all Users
def users(response):
    try:
        pass
    except Exception as e:
        return JsonResponse({'status':'false','message':"Inernal Server Error. We are sorry for inconvenience."}, status=HTTPStatus.INTERNAL_SERVER_ERROR)

    


