import requests
import json

BASE_URL = 'http://127.0.0.1:8000/api'

def test_admin_registration():
    url = f'{BASE_URL}/auth/register/'
    data = {
        'email': 'admin@example.com',
        'username': 'admin',
        'password': 'admin123',
        'password2': 'admin123',
        'first_name': 'Admin',
        'last_name': 'User'
    }
    response = requests.post(url, json=data)
    print("\nAdmin Registration Response:", response.status_code)
    print(response.json() if response.status_code != 500 else "Server Error")

def test_student_registration():
    url = f'{BASE_URL}/auth/register/'
    data = {
        'email': 'student@example.com',
        'username': 'student',
        'password': 'student123',
        'password2': 'student123',
        'first_name': 'Test',
        'last_name': 'Student'
    }
    response = requests.post(url, json=data)
    print("\nStudent Registration Response:", response.status_code)
    print(response.json() if response.status_code != 500 else "Server Error")

def test_login(email, password):
    url = f'{BASE_URL}/auth/login/'
    data = {
        'email': email,
        'password': password
    }
    response = requests.post(url, json=data)
    print("\nLogin Response:", response.status_code)
    print(response.json() if response.status_code != 500 else "Server Error")
    return response.json().get('access') if response.status_code == 200 else None

def test_create_category(token):
    url = f'{BASE_URL}/admin/categories/'
    headers = {'Authorization': f'Bearer {token}'}
    data = {
        'name': 'Programming',
        'description': 'Programming courses'
    }
    response = requests.post(url, json=data, headers=headers)
    print("\nCreate Category Response:", response.status_code)
    print(response.json() if response.status_code != 500 else "Server Error")
    return response.json().get('id') if response.status_code == 201 else None

def test_create_course(token, category_id):
    url = f'{BASE_URL}/admin/courses/'
    headers = {'Authorization': f'Bearer {token}'}
    data = {
        'title': 'Python for Beginners',
        'description': 'Learn Python programming from scratch',
        'category': category_id,
        'price': '49.99'
    }
    response = requests.post(url, json=data, headers=headers)
    print("\nCreate Course Response:", response.status_code)
    print(response.json() if response.status_code != 500 else "Server Error")

def test_list_courses():
    url = f'{BASE_URL}/courses/'
    response = requests.get(url)
    print("\nList Courses Response:", response.status_code)
    print(response.json() if response.status_code != 500 else "Server Error")

def test_student_enroll(token, course_id):
    url = f'{BASE_URL}/courses/{course_id}/enroll/'
    headers = {'Authorization': f'Bearer {token}'}
    response = requests.post(url, headers=headers)
    print("\nEnroll Course Response:", response.status_code)
    print(response.json() if response.status_code != 500 else "Server Error")

if __name__ == '__main__':
    print("Testing API endpoints...")
    
    # Test admin registration and login
    test_admin_registration()
    admin_token = test_login('admin@example.com', 'admin123')
    
    # Test student registration and login
    test_student_registration()
    student_token = test_login('student@example.com', 'student123')
    
    if admin_token:
        # Test admin operations
        category_id = test_create_category(admin_token)
        if category_id:
            test_create_course(admin_token, category_id)
    
    # Test public endpoint
    test_list_courses()
    
    # Test student enrollment
    if student_token:
        test_student_enroll(student_token, 1)  # Assuming course ID 1 