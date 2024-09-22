### Investpulse
---
This is a simple backend service or managing investment accounts 

### How it works

## Authentication

Authentication is required to access certain endpoints. The API uses token-based authentication. To authenticate a request, include an `Authorization` header with a valid JWT token.

Example:

```http
Authorization: Bearer <JWT_TOKEN>
```

### Requirements
---
- Python3 *(version 3.12.3)*
- Pyenv *(version 3.12.3)*
- Django *(version => 4.2.11)*

### Project Setup
---
#### Installation
1. Clone this repository
```bash
git clone https://github.com/ggkm3251/investment_project.git
```
2. Navigate into the project base folder
```bash
cd investment_project
```
3. Open the root folder with and IDE. See example below for VSCode
```bash
code .
```

### Project Scripts
4. Create and activate a virtual enviroment,
```bash
pyenv activate investment-project
```
5. Install project dependacies
```bash
pip install -r requirements.txt

```
6. Create *.env* files
*.env*

##### Enviroment variables
```
SECRET_KEY='django-secret-key' 
DJANGO_ENV='dev' // default for development
DEBUG=True
ALLOWED_HOSTS=provide for localhost (Should be a list)
```

Update the value of ENV var according to your local setup

8. Migrations

This command is optional as there should be no pending migrations
```bash
 python manage.py makemigrations
```

- Register models and fields to local database
```bash
 python manage.py migrate
```

9. Create the django super user
```bash
 python manage.py createsuperuser
```
Follow and fill in the prompts

10. Fire up the server
```bash
 python manage.py runserver
```

The development server should listen on [port:8000](http://127.0.0.1:8000)

Visit admin interface on: [localhost/admin](http://127.0.0.1:8000/admin/)


## Endpoints

### User Registration

- **Endpoint**: `/register`
- **Method**: POST
- **Description**: Register a new user account.
- **Request Body**:
  - `username` (string, required): The username of the new user.
  - `email` (string, required): The email address of the new user.
  - `password` (string, required): The password for the new account.
- **Response**:
  - `message` (string): A success message upon successful registration.

### User Login

- **Endpoint**: `/api/token`
- **Method**: POST
- **Description**: Log in with an existing user account.
- **Request Body**:
  - `email` (string, required): The email address of the user.
  - `password` (string, required): The user's password.
- **Response**:
  - `token` (string): A JWT token for authentication (Access and refresh).
  - `user` (object): User information.

### Create Account

- **Endpoint**: `/api/accounts`
- **Method**: POST
- **Description**: Create a new investment account.
- **Request Body**:
  - `name` (string, required): The name of the investment account.
  - `balance` (string, required): The amount balance of the account.
- **Response**:
  - `id` (integer): The unique identifier of the created note.
  - `name` (string): The name of the investment account.
  - `balance` (string): The amount balance of the account.
  - `transactions` (integer): Nested Transactions for the investment account.
  



## Error Handling

The API may return error responses with appropriate HTTP status codes. Error responses will include a `message` field with a description of the error.

**Example error response**:

```json
{
  "message": "User not found"
}
```

### Author
---
This project is designed, developed and maintained by: [Glenn Mwangi](https://github.com/ggkm3251)

###### Additional information
**Database schema:** [InvestPulse ERD](https://dbdiagram.io/d/Investpulse-ERD-66ebfd6ba0828f8aa65f9a59)
**Design thinking documentation:** [InvestPulse Doc](https://docs.google.com/document/d/1ogQx3H_r_8DNdT2i9p-zOVAvF8JmeSuo_hIa9AGmfkQ/edit?usp=sharing)

