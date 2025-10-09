#  Social Media API

A Django REST Framework–based API that powers user registration, authentication, and profile management for a social media platform.

## Setup
1. python -m venv venv  
2. venv\Scripts\activate  (or `source venv/bin/activate`)  
3. pip install -r requirements.txt  # django, djangorestframework, pillow, etc.  
4. python manage.py migrate  
5. python manage.py createsuperuser  
6. python manage.py runserver  

## Endpoints
- POST /api/accounts/register/  → Register (returns token)  
- POST /api/accounts/login/     → Login (returns token)  
- GET/PUT /api/accounts/profile/ → Profile (requires Token auth)  

## Auth
Use header:  
`Authorization: Token <token>`  

## User Model
Custom user extends **AbstractUser** with:
- `bio` (TextField)  
- `profile_picture` (ImageField)  
- `followers` (ManyToManyField to self, symmetrical=False)

##
