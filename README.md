# url-shortner
A webapp for converting a long unreadable url to a user friendly readable url.  URL generated are best for social sharing and marketing campaigns.

## how to install 
### Steps : 
1. Clone the repo using following command :
```
https://github.com/niteshverma09/url-shortner
```
2. Install requirements from `requirements.txt` 
```
pip install -r requirements.txt
```
3. create .env file and put following values in that 
```
SITE_URL=localhost:8000
DB_NAME=your_db_name
DB_USERNAME=your_db_username
DB_PASSWORD=your_db_password
DB_HOST=localhost
DB_PORT=
SECRET_KEY=your_django_generated_secret_key
DEBUG=True
```
4. Run migrations to create database tables
```
python manage.py migrate
```
5. run `python manage.py runserver` and enjoy. 
