# Udemy Clone API

A feature-rich RESTful API for a learning management platform built with Django and Django Rest Framework.

## Features

- User authentication with JWT
- Role-based access control (Student/Admin)
- Course management
- Video content management
- Student enrollment
- Course reviews and ratings
- Progress tracking
- Admin dashboard APIs
- API documentation with Swagger/ReDoc

## Tech Stack

- Python 3.8+
- Django 5.0.2
- Django Rest Framework 3.14.0
- PostgreSQL (Production) / SQLite (Development)
- JWT Authentication
- Swagger/ReDoc for API documentation

## Setup Instructions

1. Clone the repository:
```bash
git clone <repository-url>
cd udemy-clone
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
.\venv\Scripts\activate  # Windows
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Apply database migrations:
```bash
python manage.py migrate
```

5. Create a superuser:
```bash
python manage.py createsuperuser
```

6. Run the development server:
```bash
python manage.py runserver
```

## API Documentation

The API documentation is available at:
- Swagger UI: http://localhost:8000/swagger/
- ReDoc: http://localhost:8000/redoc/

## Test Credentials

### Admin User
- Email: aifunathesni@gmail.com
- Password: admin123

### Student User
- Email: student@example.com
- Password: student123

## API Endpoints

### Authentication

- POST /api/auth/register/ - Register a new user
- POST /api/auth/login/ - Login and get JWT tokens
- POST /api/auth/token/refresh/ - Refresh JWT token
- POST /api/auth/password-reset/ - Request password reset
- POST /api/auth/password-change/ - Change password
- GET/PUT /api/auth/profile/ - Get/Update user profile

### Courses (Public)

- GET /api/courses/ - List all published courses
- GET /api/courses/?search=query - Search courses
- GET /api/courses/<id>/ - Get course details

### Student Features

- POST /api/courses/<id>/enroll/ - Enroll in a course
- GET /api/my-courses/ - List enrolled courses
- GET /api/my-courses/<id>/ - View course content
- POST /api/courses/<id>/reviews/ - Create course review
- PUT/DELETE /api/reviews/<id>/ - Update/Delete own review

### Admin Features

- CRUD /api/admin/users/ - Manage users
- CRUD /api/admin/courses/ - Manage courses
- CRUD /api/admin/categories/ - Manage categories
- CRUD /api/admin/tags/ - Manage tags
- POST /api/admin/courses/<id>/modules/ - Add course modules
- POST /api/admin/modules/<id>/videos/ - Add module videos

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

 