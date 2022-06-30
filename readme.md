# Bright Money(Backend Developer Intern Task)


## Flow of the Project
1) Any user needs to signup using postman.
2) User then needs to login postman.
3) After Logging in when user clicks Link Account button, Link Token is genrated which is used to genrate the Access Token.
4) Access Token along with Item ID is Stored in the Database.
6) This Access Token is then used to find all the accounts details of the user.
7) While Creating the Link Token a web hook link is also genrated, which listens for any transaction updates.
8) User with linked Account on Plaid can get his transactions via Postman.





# API Overview



## 1. `https://bright-task.herokuapp.com/api/signup` <br>
To Reigster the user 
### Request 
```http
POST /api/signup
```

| Parameter | Type | Description |
| :--- | :--- | :--- |
| `username` | `string` | **Required**|
| `password` | `string` | **Required**|
| `name` | `string` | **Required**|

Sample Request Body in Json Form
```JSON
{
    "username":"vivekvarshney40@gmail.com",
    "password":"12345678",
    "name":"Vivek" 
}
```

Sample Response Body in Json Form
```JSON
{
    "username":"vivekvarshney40@gmail.com",
    "name":"Vivek" 
}
```




## 2. `https://bright-task.herokuapp.com/api/login` <br>
To Login the user 
### Request 
```http
POST /api/login
```

| Parameter | Type | Description |
| :--- | :--- | :--- |
| `username` | `string` | **Required**|
| `password` | `string` | **Required**|


Sample Request Body in Json Form
```JSON
{
    "username":"vivekvarshney40@gmail.com",
    "password":"12345678",
}
```

Sample Response Body in Json Form
```JSON
{
    "refresh": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTYyNjI4NzgyMiwianRpIjoiYmQ3ZTgyMTM0NmNjNDdiNzk2YTdkYzQzNjU1NDRjMzciLCJ1c2VyX2lkIjoxMH0.Hd-4MnkAezsJp0sX4gbagXuRs0q0-jmL2QUWzCf5LG8",
    "access": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNjI2MjAxNzIyLCJqdGkiOiI3OTU2NzQ2ZWRhYWY0NzkxOWZlYjZlMTdiYmM5ZmJlYSIsInVzZXJfaWQiOjEwfQ.QlqsQ5xg2BQ3cAQ7r-f9CDxTBrdhCzeYkTV8ZT5_op8"
}
```



         
## 3. `https://bright-task.herokuapp.com/api/createlinktoken` <br>
To Genrate the Link Token of the user
### Request 
```http
POST /api/createlinktoken
```
Header : Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNjI2MjAxMjg5LCJqdGkiOiI5Zjc1ODJkZjc5ZGU0M2MyYTAyNTIxNWE2MjM2YTAzMiIsInVzZXJfaWQiOjEwfQ.v3UCFK33QdUrn8HQ2XI3m1t3tqyteMvGmTZ15wCyGqE

| Parameter | Type | Description |
| :--- | :--- | :--- |
| `username` | `string` | **Required**|
| `password` | `string` | **Required**|




Sample Response Body in Json Form
```JSON
{
    "expiration": "2022-06-29T23:09:40Z",
    "link_token": "link-sandbox-82eb5c04-5cdc-47b8-b04b-c963e334599a",
    "request_id": "NxORWoOMuOnPfrw"
}
```



## 4. `https://bright-task.herokuapp.com/api/get_access_token` <br>
To Genrate the Access token of the user ans storing it to the Database
### Request 
```http
POST /api/get_access_token
```
Header : Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNjI2MjAxMjg5LCJqdGkiOiI5Zjc1ODJkZjc5ZGU0M2MyYTAyNTIxNWE2MjM2YTAzMiIsInVzZXJfaWQiOjEwfQ.v3UCFK33QdUrn8HQ2XI3m1t3tqyteMvGmTZ15wCyGqE






## 5. `https://bright-task.herokuapp.com/api/get_account` <br>
To Get the details of the all the account of the user
### Request 
```http
POST /api/get_account
```
Header : Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNjI2MjAxMjg5LCJqdGkiOiI5Zjc1ODJkZjc5ZGU0M2MyYTAyNTIxNWE2MjM2YTAzMiIsInVzZXJfaWQiOjEwfQ.v3UCFK33QdUrn8HQ2XI3m1t3tqyteMvGmTZ15wCyGqE







## 6. `https://bright-task.herokuapp.com/api/transactions/get` <br>
To Get the details of the all transactions of the user
### Request 
```http
GET /api/transations/get
```
Header : Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNjI2MjAxMjg5LCJqdGkiOiI5Zjc1ODJkZjc5ZGU0M2MyYTAyNTIxNWE2MjM2YTAzMiIsInVzZXJfaWQiOjEwfQ.v3UCFK33QdUrn8HQ2XI3m1t3tqyteMvGmTZ15wCyGqE







## 7. `https://bright-task.herokuapp.com/api/listen <br>
Web hook URl,on being triggred returns account deatils of user
### Request 
```http
POST /api/listen
```
Header : Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNjI2MjAxMjg5LCJqdGkiOiI5Zjc1ODJkZjc5ZGU0M2MyYTAyNTIxNWE2MjM2YTAzMiIsInVzZXJfaWQiOjEwfQ.v3UCFK33QdUrn8HQ2XI3m1t3tqyteMvGmTZ15wCyGqE











## Status Codes
returns the following status codes in its API:

| Status Code | Description |
| :--- | :--- |
| 200 | `OK` |
| 201 | `CREATED` |
| 400 | `BAD REQUEST` |
| 404 | `NOT FOUND` |
| 500 | `INTERNAL SERVER ERROR` |
