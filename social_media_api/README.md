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


# Posts & Comments Endpoints

GET /api/posts/                 - list posts (paginated)
POST /api/posts/                - create post (auth required)
GET /api/posts/{id}/            - retrieve post (includes comments)
PUT/PATCH /api/posts/{id}/      - update post (owner only)
DELETE /api/posts/{id}/         - delete post (owner only)

GET /api/comments/              - list comments
POST /api/comments/             - create comment (auth required)
GET/PUT/DELETE /api/comments/{id}/ - retrieve/update/delete comment (owner only)

Filtering example:
GET /api/posts/?search=keyword
GET /api/posts/?ordering=created_at
GET /api/posts/?author=1
