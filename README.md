# SJTUPlus


## How to startup

1. Install dependencies
   ```
   $ pip3 install -r requirements.txt
   ```
2. Create database
   ```
   $ python3 manage.py makemigrations
   $ python3 manage.py migrate
   ```
3. Create Superuser
   ```
   $ python3 manage.py createsuperuser
   ```
4. Load database backup 
   ```
   $ python3 manage.py loaddata /path/to/backup.json
   ```
5. Run the server
   ```
   # To run a debug server
   $ python3 manage.py runserver
   # To run a production server
   # This will collect the static resources to /static-files
   # You need another web server to host the static resources
   $ python3 manage.py collectstatics 
   $ gunicorn -c gunicorn.conf.py SJTUPlus.wsgi:application
   ```
6. Run the db watcher
   ```
   python3 manage.py watch groups
   ```
