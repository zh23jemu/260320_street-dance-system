$python = ".\.venv\Scripts\python.exe"

& $python manage.py migrate
& $python manage.py seed_demo_data
& $python manage.py runserver
