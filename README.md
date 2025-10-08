# Online-Courses

Django API (health-check, courses).  
## Setup
python -m venv venv
venv\Scripts\activate  # Windows
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
## Env (.env)
DEBUG=true
SECRET_KEY=your-secret
ALLOWED_HOSTS=127.0.0.1,localhost
