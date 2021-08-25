# Step 1

```bash
pip install -r requirements.txt
```

# Step 2
```bash
 install postgresql

 install pgadmin
  ```

# Step 3

change settings.py in shop folder

```bash
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': '',
        'USER': '',
        'PASSWORD': '',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
```
 
 
# Step 4

```bash
python3 manage.py makemigrations
python3 manage.py migrate
```
 
  
# Step 5

```bash
python3 manage.py runserver
```
 

 

